"""
Timeout with ThreadPoolExecutor
"""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Optional

from resilience_patterns_observability.policies.timeout_policy import \
    TimeoutPolicy


class TimeoutExecutor:
    """
    TimeoutExecutor - Runs the Timeout Logic
    """

    def __init__(self, timeout_policy: TimeoutPolicy) -> None:
        self.timeout_policy = timeout_policy
        self.executor = ThreadPoolExecutor(max_workers=1)

    def execute(self, func: Callable[..., Any], *args:Any, **kwargs:Any) -> (
            Any):
        """
        the function to be run is fed to the executor.
        """
        future_1 = self.executor.submit(func, *args, **kwargs)
        try:
            return future_1.result(timeout=self.timeout_policy.timeout_seconds)
        except TimeoutError as e:
            future_1.cancel()
        raise
