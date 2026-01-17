"""
    FILE: test_retry_timeout_cancellation.py
"""

import time

from resilience_full_impl.cancellation.exceptions import CancelledException
from resilience_full_impl.executor.resilience_executor import \
    ResilienceExecutor, TimeoutException
from resilience_full_impl.policy.retry_policy import RetryPolicy
from resilience_full_impl.policy.timeout_policy import TimeoutPolicy


def slow_function(token):
    """
    TEST FUNCTION
    :param token:
    :return:
    """
    for _ in range(6):
        token.throw_if_cancelled()
        time.sleep(1)
    return "SHOULD NOT OCCUR"

if __name__ == "__main__":
    retry = RetryPolicy(max_attempts=3, retry_interval_ms=100, exponential=False)
    timeout_policy = TimeoutPolicy(timeout_seconds=2)

    executor = ResilienceExecutor(retry)
    try:
        executor.execute_with_retry_and_timeout(slow_function, timeout_policy)
        print("ERROR: should have timed out")
    except (TimeoutException, CancelledException) as e:
        print("Timeout + Cancellation Propagation Correctly")

    