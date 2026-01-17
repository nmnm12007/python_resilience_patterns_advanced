"""
Defines the various failures and maps them
create an immutable Failure object for every request
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional

class FailureType(Enum):
    """
    defines the failure type
    """
    TIMEOUT = "timeout"
    CONNECTION = "connection"
    RATE_LIMIT = "rate_limit"
    VALIDATION = "validation"
    DEPENDENCY = "dependency"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class Failure:
    failure_type: FailureType
    message: str
    retryable: bool
    original_exception: Optional[Exception] = None





