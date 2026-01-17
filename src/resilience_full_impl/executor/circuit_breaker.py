import threading
import time

from resilience_full_impl.cancellation.exceptions import CancelledException


class CircuitBreakerException(Exception):
    """
    Circuit Breaker Exception
    """
    pass


class CircuitBreaker:
    """
    Thread-safe Cancellation Aware circuit breaker
    """

    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

    def __init__(self, cb_pol_obj):
        self._cb_pol_obj = cb_pol_obj
        self._state = self.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._lock = threading.Lock()

    def _before_execution(self):
        with ((self._lock)):
            if self._state == self.OPEN:
                if time.time() - self._last_failure_time >= \
                    self._cb_pol_obj.recovery_timeout:
                    self._state = self.HALF_OPEN
                else:
                    raise CircuitBreakerException("[CB]: Circuit is Still "
                                                  "OPEN")
    def _after_success(self):
        with self._lock:
            self._state = self.CLOSED
            self._failure_count = 0
    def _after_failure(self, ex : Exception):
        if isinstance(ex, CancelledException):
            return # CANCEL SHOULD NOT TRIP CIRCUIT

        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._failure_count >= self._cb_pol_obj.failure_threshold:
                self._state = self.OPEN

    
