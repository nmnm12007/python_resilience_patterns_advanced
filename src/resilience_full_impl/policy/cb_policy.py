from dataclasses import dataclass

@dataclass(frozen=True)
class CircuitBreakerPolicy:
    """
    Circuit Breaker Policy Class
    :param: failure_threshold:int
    :param: recovery_timeout:int
    """
    failure_threshold:int
    recovery_timeout:int
