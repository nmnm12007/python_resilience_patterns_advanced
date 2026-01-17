from dataclasses import dataclass

@dataclass(frozen=True)
class bulkhead_policy:
    max_concurrent_calls:int
    acquire_timeout:int
