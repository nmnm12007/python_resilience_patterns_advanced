import time

from resilience_full_impl.cancellation.cancellation_token import \
    CancellationToken
from resilience_full_impl.executor.resilience_executor import \
    ResilienceExecutor
from resilience_full_impl.policy.retry_policy import RetryPolicy
from resilience_full_impl.policy.timeout_policy import TimeoutPolicy


def slow_function(token:CancellationToken):
    """
              TEST function 
    :return:
    """
    for _ in range(6):
        token.throw_if_cancelled()
        time.sleep(0.5)     
    return "DONE SUCCESSFUL"


if __name__ == "__main__":
    retry_policy = RetryPolicy(3, 5, True)
    timeout_policy = TimeoutPolicy(2)
    executor = ResilienceExecutor(retry_policy)
    executor.execute_with_retry_and_timeout(slow_function, timeout_policy)
