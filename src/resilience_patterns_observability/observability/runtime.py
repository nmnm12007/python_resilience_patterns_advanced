"""
Observability Shared Instrumentation helpers
"""

from resilience_patterns_observability.observability.context import current_span
from resilience_patterns_observability.observability.inmemory_metrics import InMemoryMetricsCollector

metrics = InMemoryMetricsCollector()

def get_current_span():
    """

    :return:
    """
    return current_span().get()

