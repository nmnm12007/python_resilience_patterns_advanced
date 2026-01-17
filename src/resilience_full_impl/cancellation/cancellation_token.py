import time
import threading
from typing import Optional
from resilience_full_impl.cancellation.exceptions import \
                CancelledException

class CancellationToken:
    """
        Cooperative cancellation & deadline token.

        - Supports explicit cancellation
        - Supports deadline-based cancellation
        - Thread-safe
    """

    def __init__(self, deadline_seconds: Optional[float] = None) -> None:
        self._deadline = (
            time.time() + deadline_seconds if deadline_seconds is not None
            else None)
        self._cancelled = False
        self._lock = threading.Lock()

    def cancel(self) -> None:
        """
        Explicitly cancel the token
        :return:
        """
        with self._lock:
            self._cancelled = True

    def is_cancelled(self) -> bool:
        """
        check if the token is canceled
        - explicit cancel()
        - deadline exceeded
        :return:
        """
        if self._deadline is not None and time.time() >= self._deadline:
            return True
        with self._lock:
            return self._cancelled

    def throw_if_cancelled(self) -> None:
        """
        Raise CancelledException if the token is canceled

        :return:
        """
        if self.is_cancelled():

            raise CancelledException(
                "Operation canceled or Deadline exceeded"
            )
        
