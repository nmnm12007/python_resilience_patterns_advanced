"""
Observability = Tracing
"""

from contextlib import contextmanager
import time

class TraceSpan:
    """
        TraceSpan
    """
    def __init__(self, name: str, attributes: dict | None = None):
        self.duration_ms = None
        self.name = name
        self.attributes = attributes or {}
        self.start_time = time.time()

    def set_attribute(self, key, value):
        """

        :param key:
        :param value:
        """
        self.attributes[key] = value

    def end_span(self):
        """
        
        :return: 
        """
        self.duration_ms = (time.time() - self.start_time) * 1000
        


@contextmanager
def start_span(name: str, **attrs):
    """

    :param name:
    :param attrs:
    """
    span = TraceSpan(name, attrs) 
    try:
        yield span
    finally:
        TraceSpan.end_span(span)


