"""
class that defines bulkhead policy
"""


class BulkheadPolicy:
    """
    @param: max_concurrent_calls:int
    @param: acquire_timeout: int
    """

    def __init__(self, max_concurrent_calls: int = 5, acquire_timeout: int =
    0) -> None:
        self.max_concurrent_calls = max_concurrent_calls
        self.acquire_timeout = acquire_timeout
