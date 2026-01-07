"""
class tha holds bulkhead specific items
"""

from threading import Semaphore

from resilience_patterns_observability.policies.bulkhead_policy import BulkheadPolicy


class Bulkhead:
    """
    includes Semaphore, acquire_timeout and max_concurrent_calls
    """

    def __init__(self, policy: BulkheadPolicy):
        self.semaphore = Semaphore(policy.max_concurrent_calls)
        self.acquire_timeout = policy.acquire_timeout
