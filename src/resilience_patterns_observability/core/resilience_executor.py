"""
Implements Resilience Executor
"""

import logging
import time
from functools import wraps
from typing import Optional, Callable, Any

from resilience_patterns_observability.core.bulkhead import Bulkhead
from resilience_patterns_observability.core.execution_context import ExecutionContext
from resilience_patterns_observability.core.timeout_executor import TimeoutExecutor
from resilience_patterns_observability.policies.bulkhead_policy import BulkheadPolicy
from resilience_patterns_observability.policies.cb_policy import CircuitBreakerPolicy
from resilience_patterns_observability.policies.cb_state import CircuitBreakerState
from resilience_patterns_observability.policies.retry_policy import \
    RetryPolicy, before_retry_attempt, after_retry_attempt
from resilience_patterns_observability.policies.timeout_policy import TimeoutPolicy

from resilience_patterns_observability.observability.context import (
    current_span, current_trace_id)
from resilience_patterns_observability.observability.inmemory_tracing import \
    InMemoryTraceSpan
from resilience_patterns_observability.observability.runtime import metrics



logger = logging.getLogger(__name__)


class ResilienceExecutor:
    """
    Orchestrates Retry, Circuit Breaker, Bulkhead, and Timeout patterns.
    """

    def __init__(
        self,
        retry_policy: RetryPolicy,
        cb_policy: CircuitBreakerPolicy,
        bulkhead_policy: BulkheadPolicy,
        timeout_policy: TimeoutPolicy,
    ) -> None:
        self.retry_policy: RetryPolicy = retry_policy
        self.cb_policy: CircuitBreakerPolicy = cb_policy
        self.bulkhead_policy: BulkheadPolicy = bulkhead_policy
        self.timeout_policy: TimeoutPolicy = timeout_policy

        self.cb_state: CircuitBreakerState = CircuitBreakerState()
        self.bulkhead: Bulkhead = Bulkhead(bulkhead_policy)
        self.timeout_executor: TimeoutExecutor = TimeoutExecutor(timeout_policy)

    def execute(self, func: Callable[..., Any], *args: Any,
                **kwargs: Any) -> Any:
        ctx = ExecutionContext()

        parent_span = current_span.get()
        trace_id = current_trace_id.get()

        root_span = InMemoryTraceSpan(
            name="resilience_executor.execute",
            trace_id=trace_id,
            parent_span_id=parent_span.span_id if parent_span else None,
        )

        span_token = current_span.set(root_span)
        trace_token = current_trace_id.set(root_span.trace_id)

        root_span.start()
        start_time = time.time()

        try:
            acquired = self.bulkhead.semaphore.acquire(
                timeout=self.bulkhead.acquire_timeout
            )
            if not acquired:
                raise RuntimeError("[BK] Bulkhead limit exceeded")

            try:
                if self._is_circuit_open():
                    raise RuntimeError("[CB] Circuit is OPEN (fail-fast)")

                last_exception: Optional[Exception] = None

                for ctx.attempt in range(1, self.retry_policy.max_retries + 1):
                    logger.debug(
                        f"[RE][{ctx.req_id}] Attempt {ctx.attempt}/"
                        f"{self.retry_policy.max_retries}"
                    )

                    retry_span = before_retry_attempt(ctx.attempt)

                    try:
                        result = self.timeout_executor.execute(func, *args,
                                                               **kwargs)
                        self._on_success(ctx)
                        return result

                    except Exception as exc:
                        self._on_failure(ctx, exc)
                        root_span.record_error(exc)
                        metrics.inc_counter(
                            "request_failure_total",
                            tags={"exception":type(exc).__name__},
                        )
                        last_exception = exc

                        if ctx.attempt == self.retry_policy.max_retries:
                            break

                        time.sleep(self.retry_policy.delay_seconds)

                    finally:
                        after_retry_attempt(retry_span)

                # retries exhausted
                raise last_exception or RuntimeError("[RE] Execution failed")

            finally:
                self.bulkhead.semaphore.release()

        finally:
            duration_ms = (time.time() - start_time) * 1000
            metrics.observe_latency(
                "request_latency_ms",
                duration_ms,
                tags={"executor":"resilience_full_impl"},
            )
            root_span.end()
            current_span.reset(span_token)
            current_trace_id.reset(trace_token)

    def _is_circuit_open(self) -> bool:
        if self.cb_state.state != "OPEN":
            return False

        elapsed:Optional[float] = time.time() - self.cb_state.last_failure_time
        logger.debug(
            f"[CB] OPEN for {elapsed:.2f}s "
            f"(recovery={self.cb_policy.recovery_timeout}s)"
        )

        if elapsed >= self.cb_policy.recovery_timeout:
            self.cb_state.state = "HALF_OPEN"
            logger.info("[CB] State transition: OPEN → HALF_OPEN")
            return False

        return True

    def _on_success(self, ctx: ExecutionContext) -> None:
        logger.debug(
            f"[CB][{ctx.req_id}] Attempt {ctx.attempt} succeeded"
        )

        if self.cb_state.state == "HALF_OPEN":
            logger.info("[CB] State transition: HALF_OPEN → CLOSED")

        self.cb_state.state = "CLOSED"
        self.cb_state.failure_count = 0

    def _on_failure(self, ctx: ExecutionContext, exc: Exception) -> None:
        self.cb_state.failure_count += 1
        self.cb_state.last_failure_time = time.time()
        ctx.last_exception = exc

        logger.error(
            f"[CB][{ctx.req_id}] Attempt {ctx.attempt} failed: {exc}"
        )

        if self.cb_state.failure_count >= self.cb_policy.failure_threshold:
            self.cb_state.state = "OPEN"
            logger.error("[CB] State transition: CLOSED → OPEN")


def resilient(
    retry_policy: RetryPolicy,
    cb_policy: CircuitBreakerPolicy,
    bulkhead_policy: BulkheadPolicy,
    timeout_policy: TimeoutPolicy,
) -> Any:
    """
    Resilience decorator factory.
    """
    executor = ResilienceExecutor(
        retry_policy, cb_policy, bulkhead_policy, timeout_policy
    )

    def decorator(func: Callable[..., Any]) -> Any:
        """ decorator factory """
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            wrapper decorator factory
            :param args:
            :param kwargs:
            :return:
            """
            return executor.execute(func, *args, **kwargs)

        return wrapper

    return decorator