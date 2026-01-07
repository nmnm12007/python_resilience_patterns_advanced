"""
class that holds the current state of the CB
"""


class CircuitBreakerState:
    """
    state : "CLOSED", "HALF-OPEN", "OPEN"
    failure_count-> int : Counter to track how many times the downstream api
    attempt failed
    last_failure_time -> datetime
    """

    def __init__(self) -> None:
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_failure_time = None
