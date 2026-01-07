"""
class that defines the Circuit Breaker Policy parameters
"""


class CircuitBreakerPolicy:
    """
    Class that holds the Circuit Breaker Policy parameters
    failure_threshold: int
    recovery_threshold: int
    """

    def __init__(self, failure_threshold: int = 3, recovery_timeout: int =
    10) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
