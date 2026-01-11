"""
In-memory metrics
"""
import logging
import threading
from collections import defaultdict
from typing import Dict, Tuple, Optional

from resilience_patterns_observability.observability.metrics import \
    MetricsCollector

logger = logging.getLogger(__name__)


class InMemoryMetricsCollector(MetricsCollector):
    """
    In-memory metrics store for local dev and testing
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: Dict[Tuple[str, frozenset], int] = defaultdict(int)
        self._latencies: Dict[
            Tuple[str, frozenset], list[float]] = defaultdict(float)
        self._gauges: Dict[Tuple[str, frozenset], float] = {}

    def _key(self, name: str, tags: Optional[Dict[str, str]]) -> Tuple[str,
    frozenset]:
        return name, frozenset((tags or {}).items())

    def inc_counter(
            self,
            name: str,
            value: int = 1,
            tags: Optional[Dict[str, str]] = None,
    ) -> None:
        key = self._key(name, tags)
        with self._lock:
            self._counters[key] += value

        logger.info(
            "METRIC counter=%s value=%s tags=%s",
            name,
            value,
            tags,
        )

    def observe_latency(
            self,
            name: str,
            duration_ms: float,
            tags: Optional[Dict[str, str]] = None,
    ) -> None:
        key = self._key(name, tags)
        with self._lock:
            self._latencies[key].append(duration_ms)

        logger.info(
            "METRIC latency=%s duration_ms=%.2f tags=%s",
            name,
            duration_ms,
            tags,
        )

    def set_gauge(
            self,
            name: str,
            value: float,
            tags: Optional[Dict[str, str]] = None,
    ) -> None:
        key = self._key(name, tags)
        with self._lock:
            self._gauges[key] = value

        logger.info(
            "METRIC gauge=%s value=%.2f tags=%s",
            name,
            value,
            tags,
        )
