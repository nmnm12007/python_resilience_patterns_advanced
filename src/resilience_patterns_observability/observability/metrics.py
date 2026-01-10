"""
MetricsCollector

Used for collecting stat data
----------------------------

Metrics We MUST Support
Pattern	Metric	Why
Retry	retry_attempt_total	Detect retry storms
Retry	retry_exhausted_total	Downstream failure
CB	circuit_state_change	Trip analysis
CB	circuit_open_duration	MTTR
Bulkhead	bulkhead_rejected_total	Capacity issue
Timeout	request_timeout_total	SLA breach
ALL	request_latency_ms	SLO
ALL	request_failure_total{type}	Error taxonomy

"""

from abc import ABC, abstractmethod
from typing import Optional, Dict


class MetricsCollector(ABC):
    """
    Vendor neutral metrics collector
    """
    @abstractmethod
    def inc_counter(self,
                    name: str,
                    value: int=1,
                    tags: Optional[Dict[str, str]]=None) -> None:
        """

        :param name:
        :param value:
        :param tags:
        """

        pass

    @abstractmethod
    def observe_latency(self,
                        name: str,
                        duration_ms: float,
                        tags: Optional[Dict[str, str]]=None,
                        )->None:
        """

        :param name:
        :param duration_ms:
        :param tags:
        :return:
        """
        pass

    @abstractmethod
    def set_gauge(self,
                  name: str, value: float,
                  tags: Optional[Dict[str, str]]=None,
                  ) -> None:
        """
        
        :param name:
        :param value:
        :param tags:
        :return:
        """
        pass

