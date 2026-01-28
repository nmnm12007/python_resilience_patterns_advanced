from resilience_full_impl.observability.logging import logger
from resilience_full_impl.observability.metrics import MetricsCollector
from resilience_full_impl.policy.bulkhead_policy import BulkheadPolicy
import threading

class BulkheadRejectedException(Exception):
    """
        Bulk head rejected exception
    """
    pass


class Bulkhead:
    """
            Bulk Head Definition
    """
    def __init__(self,
                 bulkhead_pol: BulkheadPolicy,
                 metrics: MetricsCollector):

        self._semaphore = threading.Semaphore(
            bulkhead_pol.max_concurrent_calls
        )
        self._metrics = metrics

    def acquire(self, dependency_name: str):
        """

        :param dependency_name:
        """
        acquired = self._semaphore.acquire(blocking=False)

        if not acquired:
            self._metrics.increment(
                "bulkhead_rejections_total",
                tags={"dependency_name":dependency_name}

            )
            logger.warning(
                "[BULKHEAD] : Bulkhead Rejected due to : %s", dependency_name)

            raise BulkheadRejectedException("Bulkhead Limit Exceeded")

    def release(self):
        """
               semaphore release
        """
        self._semaphore.release()


