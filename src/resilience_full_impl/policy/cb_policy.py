from dataclasses import dataclass

@dataclass(frozen=True)
class cb_policy:
    failure_threshold:int
    recovery_timeout:int
