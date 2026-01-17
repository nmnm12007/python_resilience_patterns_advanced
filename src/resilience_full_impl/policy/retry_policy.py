from dataclasses import dataclass

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts:int
    retry_interval_ms:int
    exponential:bool


