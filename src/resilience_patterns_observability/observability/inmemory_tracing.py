"""
In-memory tracing
"""
# observability/inmemory_tracing.py
import logging
import time
import uuid
from typing import Any, Dict, List

from resilience_patterns_observability.observability.tracing import TraceSpan

logger = logging.getLogger(__name__)


class InMemoryTraceSpan(TraceSpan):
    """
    In-memory trace span for local tracing.
    """

    def __init__(self, name: str, trace_id: str | None = None,
                 parent_span_id: str | None = None) -> None:
        self.name = name
        self.trace_id = trace_id or str(uuid.uuid4())
        self.parent_span_id = parent_span_id
        self.span_id = str(uuid.uuid4())
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.annotations: List[Dict[str, Any]] = []
        self.error: str | None = None


    def start(self) -> None:
        self.start_time = time.time()
        logger.info(
            "SPAN start name=%s trace_id=%s span_id=%s",
            self.name,
            self.trace_id,
            self.span_id,
        )


    def annotate(self, key: str, value: Any) -> None:
        event = {
            "ts":time.time(),
            "key":key,
            "value":value,
        }
        self.annotations.append(event)

        logger.info(
            "SPAN annotate trace_id=%s span_id=%s parent_span_id=%s  key=%s value=%s",
            self.trace_id,
            self.span_id,
            self.parent_span_id,
            key,
            value,
        )


    def record_error(self, error: Exception) -> None:
        self.error = repr(error)
        logger.exception(
            "SPAN error trace_id=%s span_id=%s",
            self.trace_id,
            self.span_id,
        )


    def end(self) -> None:
        self.end_time = time.time()
        duration_ms = (self.end_time - (
                self.start_time or self.end_time)) * 1000

        logger.info(
            "SPAN end name=%s trace_id=%s span_id=%s duration_ms=%.2f",
            self.name,
            self.trace_id,
            self.span_id,
            duration_ms,
        )
