from dataclasses import dataclass

@dataclass(frozen=True)
class BulkheadPolicy:
    """
    Bulkhead policy
    """
    max_concurrent_calls:int
    acquire_timeout:int
