import time
import threading
import pytest

from resilience_full_impl import executor
from resilience_full_impl.cancellation.cancellation_token import \
    CancellationToken
from resilience_full_impl.executor.bulkhead import BulkheadRejectedException
from resilience_full_impl.executor.resilience_executor import \
    ResilienceExecutor

from resilience_full_impl.policy.bulkhead_policy import BulkheadPolicy
from resilience_full_impl.policy.cb_policy import CircuitBreakerPolicy
from resilience_full_impl.policy.retry_policy import RetryPolicy
from resilience_full_impl.policy.timeout_policy import TimeoutPolicy

def slow_function(token: CancellationToken) -> str:
    """
    TEST FUNCTION
    :param token:
    :return:
    """
    for _ in range(6):
        token.throw_if_cancelled()
        time.sleep(1)
    return "SHOULD NOT OCCUR"


def test_bulkhead_rejects_second():
    """
       GIVEN bulkhead max_concurrent_calls = 1
       WHEN two concurrent calls are made
       THEN second call must be rejected
    """



    bulkhead_policy = BulkheadPolicy(max_concurrent_calls=1, acquire_timeout=1)

    executor = ResilienceExecutor(retry_policy=RetryPolicy(max_attempts=1,
                                                           retry_interval_ms=100,
                                                           exponential=False),
                                  cb_policy=CircuitBreakerPolicy(
                                      failure_threshold=5, recovery_timeout=5),
                                  bulk_head_policy= bulkhead_policy,
                                  )
    timeout_policy = TimeoutPolicy(timeout_seconds=10)

    exceptions = []


    def first_call():
        """
             FIRST CALL
        """
        executor.execute(slow_function, timeout_policy,
                         dependency_name="test_api")


    def second_call():
        """
            SECOND CALL
        :return:
        """
        try:
            executor.execute(slow_function, timeout_policy,
                             dependency_name="test_api")
        except Exception as e:
            exceptions.append(e)


        t1 = threading.Thread(target=first_call)
        t2 = threading.Thread(target=second_call)

        t1.start()
        time.sleep(0.2)
        t2.start()

        t1.join()
        t2.join()

        assert len(exceptions) == 1

        assert isinstance(exceptions[0], BulkheadRejectedException)

        assert (
                ("bulkhead_rejections_total", (("dependency", "test_api"),
                                               )) in
                executor._metrics._counters)
