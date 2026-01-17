from dataclasses import dataclass

@dataclass(frozen=True)
class TimeoutPolicy:
    timeout_seconds:int
