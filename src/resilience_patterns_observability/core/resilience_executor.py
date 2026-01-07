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
from resilience_patterns_observability.policies.retry_policy import RetryPolicy
from resilience_patterns_observability.policies.timeout_policy import TimeoutPolicy

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

    def execute(self, func: Callable[..., Any], *args:Any, **kwargs:Any) -> (
            Any):
        """
        Executes a function with full resilience protections.
        """
        ctx = ExecutionContext()
        logger.debug(
            f"[RE]:[{ctx.timestamp}] Executing {func.__name__} "
            f"(req_id={ctx.req_id})"
        )

        acquired = self.bulkhead.semaphore.acquire(
            timeout=self.bulkhead.acquire_timeout
        )
        if not acquired:
            raise RuntimeError("[BK] Bulkhead limit exceeded")

        try:
            if self._is_circuit_open():
                raise RuntimeError("[CB] Circuit is OPEN (fail-fast)")

            while ctx.attempt < self.retry_policy.max_retries:
                ctx.attempt += 1
                logger.debug(
                    f"[RE][{ctx.req_id}] Attempt {ctx.attempt}/"
                    f"{self.retry_policy.max_retries}"
                )

                try:
                    result = self.timeout_executor.execute(func, *args, **kwargs)
                    self._on_success(ctx)
                    return result

                except Exception as exc:
                    self._on_failure(ctx, exc)

                    if ctx.attempt >= self.retry_policy.max_retries:
                        raise

                    time.sleep(self.retry_policy.delay_seconds)

        finally:
            self.bulkhead.semaphore.release()

        raise RuntimeError("[RE] Execution failed after retries")

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
        self.cb_state.last_failure_time:Optional[float] = time.time()
        ctx.last_exception:Optional[Exception] = exc

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






# """
# Implements Resilience Executor
# """
#
# import logging
# import time
# from functools import wraps
# from typing import Optional
#
# from resilience_patterns_observability.core.bulkhead import Bulkhead
# from resilience_patterns_observability.core.execution_context import \
#     ExecutionContext
# from resilience_patterns_observability.core.timeout_executor import \
#     TimeoutExecutor
# from resilience_patterns_observability.policies.bulkhead_policy import \
#     BulkheadPolicy
# from resilience_patterns_observability.policies.cb_policy import \
#     CircuitBreakerPolicy
# from resilience_patterns_observability.policies.cb_state import \
#     CircuitBreakerState
# from resilience_patterns_observability.policies.retry_policy import RetryPolicy
# from resilience_patterns_observability.policies.timeout_policy import \
#     TimeoutPolicy
#
# logger = logging.getLogger(__name__)
#
#
# class ResilienceExecutor:
#     """
#     Implements Resilience Executor policy/state
#     """
#
#     def __init__(self, retry_policy: RetryPolicy,
#                  cb_policy: CircuitBreakerPolicy,
#                  bulkhead_policy: BulkheadPolicy,
#                  timeout_policy: TimeoutPolicy):
#         self.retry_policy:Optional[RetryPolicy] = retry_policy
#         self.cb_policy:Optional[CircuitBreakerPolicy] = cb_policy
#         self.bulkhead_policy:Optional[BulkheadPolicy] = bulkhead_policy
#         self.timeout_policy:Optional[TimeoutPolicy] = timeout_policy
#
#         self.cb_state:Optional[CircuitBreakerState] = CircuitBreakerState()
#         self.bulkhead:Optional[Bulkhead] = Bulkhead(bulkhead_policy)
#         self.timeout_executor:Optional[TimeoutExecutor] = TimeoutExecutor(timeout_policy)
#
#     def execute(self, func, *args, **kwargs):
#         """
#         Implements Resilience Executor Logic
#         """
#         ctx = ExecutionContext()
#         logger.debug(f"[RE]:[{ctx.timestamp}] : Executing {func.__name__}")
#         # DONT USE THIS :: with self.bulkhead.semaphore.acquire(  # REFER TO
#         # THE CHAT DISCUSSIONS
#         acquired = self.bulkhead.semaphore.acquire(
#             timeout=self.bulkhead.acquire_timeout)
#         if not acquired:
#             raise RuntimeError(
#                 "[BK] : Bulkhead Limit Exceeded, Try again later")
#         if self._is_circuit_open():
#             logger.debug("[CB] : Circuit Breaker State is OPEN")
#             raise RuntimeError("[CB] : Circuit Breaker State is OPEN")
#         while ctx.attempt < self.retry_policy.max_retries:
#             ctx.attempt += 1
#             logger.debug(
#                 "[CB]: REQUEST:{ctx.req_id} :attempt #: "
#                 "{ctx.attempt} out of {"
#                 "self.retry_policy.max_retries}:"
#                 " at {ctx.timestamp}: is done."
#             )
#             try:
#                 # result = func(*args, **kwargs)
#                 result = self.timeout_executor.execute(func, *args, **kwargs)
#                 self._on_success()
#                 return result
#             except Exception as e:
#                 self._on_failure(ctx, e)
#                 time.sleep(self.retry_policy.delay_seconds)
#
#                 if ctx.attempt >= self.retry_policy.max_retries:
#                     raise
#
#             finally:
#                 self.bulkhead.semaphore.release()
#
#         raise RuntimeError("[CB]:Failure with Exception:{e}")
#
#     def _is_circuit_open(self):
#         if self.cb_state.state == "OPEN":
#             logger.debug(
#                 "[CB]:Circuit Breaker State is OPEN, Fail-Fast now, "
#                 "Try again later")
#             elapsed_time = time.time() - self.cb_state.last_failure_time
#             if elapsed_time >= self.cb_policy.recovery_timeout:
#                 self.cb_state.state = "HALF_OPEN"
#                 logger.debug("[CB]:State Transition :: OPEN -> HALF-OPEN")
#                 return False
#             logger.debug("[CB]:Current State : {cb_state.state}")
#             return True
#         return False
#
#     def _on_success(self) -> None:
#         logger.debug(
#             "[CB]: Attempt {ctx.attempt} out of {"
#             "self.retry_policy.max_retries} is a success."
#         )
#         if self.cb_state.state == "HALF_OPEN":
#             logger.info("[CB] : State Transition :: HALF-OPEN -> CLOSED")
#         self.cb_state.state = "CLOSED"
#         self.cb_state.failure_count = 0
#
#     def _on_failure(self, ctx, e):
#         self.cb_state.failure_count += 1
#         self.cb_state.last_failure_time = ctx.timestamp
#         ctx.last_exception = e
#         logger.error(
#             "[CB]:[{ctx.timestamp}]:Attempt {ctx.attempt} out of {"
#             "self.retry_policy.max_retries} failed with {ctx.last_exception}."
#         )
#         if self.cb_state.failure_count >= self.cb_policy.failure_threshold:
#             self.cb_state.state = "OPEN"
#         logging.error(
#             "[CB]: State Transition :: CLOSED -> OPEN done. Current State : "
#             "{cb_state.state}"
#         )
#
#
# def resilient(
#         retry_policy: RetryPolicy,
#         cb_policy: CircuitBreakerPolicy,
#         bulkhead_policy: BulkheadPolicy,
#         timeout_policy: TimeoutPolicy,
# ):
#     """
#     definition and implementation of Resilience Decorator
#     """
#
#     executor = ResilienceExecutor(retry_policy, cb_policy, bulkhead_policy,
#                                   timeout_policy)
#
#     def decorator(func):
#         """
#         Decorator for Resilience Decorator
#         """
#
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             """
#             Wrapper for Resilience Decorator
#             """
#             result = executor.execute(func, *args, **kwargs)
#             return result
#
#         return wrapper
#
#     return decorator
