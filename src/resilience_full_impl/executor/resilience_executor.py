"""
    Resilience Executor for retry, timeout
"""
import threading
import time
from typing import TypeVar, Callable

from resilience_full_impl.cancellation.cancellation_token import \
    CancellationToken
from resilience_full_impl.cancellation.exceptions import CancelledException
from resilience_full_impl.executor.circuit_breaker import CircuitBreaker
from resilience_full_impl.executor.execution_context import \
    ExecutionContext
from resilience_full_impl.policy.cb_policy import CircuitBreakerPolicy
from resilience_full_impl.policy.retry_policy import RetryPolicy
from resilience_full_impl.policy.timeout_policy import TimeoutPolicy

T = TypeVar("T")


class TimeoutException(Exception):
    """
    Exception raised when a timeout occurs
    """
    pass


class ResilienceExecutor:
    """
         Implements ResilienceExecutor for retry, timeout
    """

    def __init__(self, retry_policy: RetryPolicy,
                 cb_policy: CircuitBreakerPolicy, ):
        self._retry_policy = retry_policy
        self._cb_obj = CircuitBreaker(cb_pol_obj=cb_policy)

    def _sleep_before_next_attempt(self, attempt: int) -> None:
        delay_ms = self._retry_policy.retry_interval_ms

        if self._retry_policy.exponential:
            delay_ms = delay_ms * 2 ** (attempt - 1)

        time.sleep(delay_ms / 1000)

    def execute(self,
                func: Callable[[CancellationToken], T],
                timeout_policy: TimeoutPolicy, ) -> T:
        """

        :param func:
        :param timeout_policy:
        :return:
        """
        self._validate_policies(self._retry_policy, timeout_policy)
        token = CancellationToken(
            deadline_seconds=timeout_policy.timeout_seconds)

        ctx = ExecutionContext(retry_pol=self._retry_policy,
                               timeout_pol=timeout_policy,
                               token=token,
                               cb=self._cb_obj)

        return self._execute_with_retry(func, ctx)

    def _execute_with_retry(self, func: Callable[[CancellationToken], T],
                            ctx: ExecutionContext
                            ) -> T:
        """

        :param func:
        :return: 
        """
        last_exception = None

        for attempt in range(1, self._retry_policy.max_attempts + 1):
            ctx.token.throw_if_cancelled()
            ctx.cb.before_execution()

            from resilience_full_impl.executor.circuit_breaker import \
                CircuitBreakerException
            try:
                result_success = self._execute_with_timeout(func, ctx)
                ctx.cb.after_success()
                return result_success

            except (CircuitBreakerException, CancelledException,) as e:
                raise  # what is the order of exceptions

            except Exception as e:
                last_exception = e
                ctx.cb.after_failure(e)

            if attempt == ctx.retry_pol.max_attempts:
                break

            self._sleep_before_next_attempt(attempt)
        raise last_exception

    def _execute_with_timeout(self, func: Callable[[CancellationToken], T],
                              ctx: ExecutionContext) -> T:
        """
        
        :param func:
        :param ctx:
        :return:
        """
        result_container = {}
        exception_container = {}

        def target():
            """
                 Target method for executing function
            """
            try:
                result_container["result"] = func(ctx.token)
            except Exception as e:
                exception_container["exception"] = e

        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        thread.join(timeout=ctx.timeout_pol.timeout_seconds)
        if thread.is_alive():
            ctx.token.cancel()
            raise TimeoutException(f"Timed out after "
                                   f"{ctx.timeout_pol.timeout_seconds} "
                                   f"seconds")

        if "exception" in exception_container:
            raise exception_container["exception"]

        return result_container.get("result")

    def _validate_policies(self, retry_policy: RetryPolicy,
                           timeout_policy: TimeoutPolicy) -> None:
        """

        :param retry_policy:
        :param timeout_policy:
        :return:
        """
        # max_possible_time = (retry_policy.max_attempts *
        #                      timeout_policy.timeout_seconds)
        if timeout_policy.timeout_seconds <= 0:
            raise ValueError(
                "[TimeoutPolicy] : timeout_policy.timeout_seconds <= 0")
        if retry_policy.max_attempts <= 0:
            raise ValueError("[TimeoutPolicy] : retry_policy.max_attempts "
                             "<= 0")
