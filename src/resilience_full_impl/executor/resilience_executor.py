"""
    Resilience Executor for retry, timeout
"""
import threading
import time
from typing import TypeVar, Callable

from resilience_full_impl.cancellation.cancellation_token import \
    CancellationToken
from resilience_full_impl.cancellation.exceptions import CancelledException
from resilience_full_impl.policy.retry_policy import RetryPolicy
from resilience_full_impl.policy.timeout_policy import TimeoutPolicy
from resilience_patterns_observability.policies.cb_policy import \
    CircuitBreakerPolicy

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
                 cb_policy_obj: CircuitBreakerPolicy):
        self._retry_policy = retry_policy
        self._cb_policy_obj = cb_policy_obj

    def _sleep_before_next_attempt(self, attempt: int) -> None:
        delay_ms = self._retry_policy.retry_interval_ms

        if self._retry_policy.exponential:
            delay_ms = delay_ms * 2 ** (attempt - 1)

        time.sleep(delay_ms / 1000)

    def _execute_with_retry(self, func: Callable[[CancellationToken], T],
                            token: CancellationToken
                            ) -> T:
        """

        :param func:
        :return: 
        """
        last_exception = None

        for attempt in range(1, self._retry_policy.max_attempts + 1):
            token.throw_if_cancelled()
            try:
                return func(token)
            except CancelledException as e:
                raise
            except Exception as e:
                last_exception = e

            if attempt == self._retry_policy.max_attempts:
                break

            self._sleep_before_next_attempt(attempt)
        raise last_exception

    def _execute_with_timeout(self, func: Callable[[CancellationToken], T],
                              token: CancellationToken,
                              timeout_policy: TimeoutPolicy) -> T:
        """
        :rtype: T
        :param timeout_policy:
        :param func:
        :return:
        """
        result_container = {}
        exception_container = {}

        def target():
            """
                 Target method for executing function
            """
            try:
                result_container["result"] = func(token)
            except Exception as e:
                exception_container["exception"] = e

        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        thread.join(timeout=timeout_policy.timeout_seconds)
        if thread.is_alive():
            token.cancel()
            raise TimeoutException(f"Timed out after "
                                   f"{timeout_policy.timeout_seconds} seconds")

        if "exception" in exception_container:
            raise exception_container["exception"]

        return result_container.get("result")

    def execute_with_retry_and_timeout(self,
                                       func: Callable[[CancellationToken], T],
                                       timeout_policy: TimeoutPolicy,
                                       ) -> T:
        """

        :param func:
        :param timeout_policy:
        :return:
        """
        token_1 = CancellationToken(
            deadline_seconds=timeout_policy.timeout_seconds)

        def timed_func(token_1: CancellationToken) -> T:
            """

            :return:
            """
            return self._execute_with_timeout(func, token_1, timeout_policy)

        return self._execute_with_retry(timed_func, token_1)
