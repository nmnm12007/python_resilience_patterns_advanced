"""
Observability - Metrics
"""

from collections import defaultdict


class MetricsCollector:
    """
    Observability - Metrics
    """

    def __init__(self):
        self._counters = defaultdict(int)

    def increment(self, name: str, tags: dict | None = None):
        """
        
        :param name:
        :param tags:
        :return:
        """
        key = (name, tuple(sorted((tags or {}).items())))
        self._counters[key] += 1
