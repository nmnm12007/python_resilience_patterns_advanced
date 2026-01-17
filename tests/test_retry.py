
from resilience_full_impl.executor.resilience_executor import \
    ResilienceExecutor
from resilience_full_impl.policy.retry_policy import RetryPolicy


counter = {"count" : 0}

def flaky_function() -> str:
    """

    :return:
    """
    counter["count"] += 1
    print("Attempt:",counter["count"])
    if counter["count"] < 3:
        raise RuntimeError("Flaky function: Temporary ")
    return "SUCCESS"


if __name__ == "__main__":
    RetryPolicyObj = RetryPolicy(3, 2, True)
    executor = ResilienceExecutor(RetryPolicyObj)

    result = executor.execute_with_retry(flaky_function)
    print(result)

    