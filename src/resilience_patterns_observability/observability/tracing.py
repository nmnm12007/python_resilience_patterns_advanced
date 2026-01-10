"""
TraceSpan models one logical operation:
start()
 ├── annotate("retry_attempt", 2)
 ├── annotate("circuit_state", "OPEN")
 ├── error(exception)
 └── end()

"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class TraceSpan(ABC):
    """
    TraceSpan for single
    """


    @abstractmethod
    def start(self) -> None:
        """
        start
        :return:
        """
        pass

    @abstractmethod
    def annotate(self, key: str, value: Any) -> None:
        """
        annotate
        :param key:
        :param value:
        :return:
        """
        pass

    @abstractmethod
    def record_error(self, error: Exception) -> None:
        """
        record_error
        :param error:
        :return:
        """
        pass

    @abstractmethod
    def end(self) -> None:
        """

        :return:
        """
        pass

    