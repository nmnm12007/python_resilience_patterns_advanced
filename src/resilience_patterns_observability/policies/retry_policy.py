"""
define retry policy
@param: max_retries: int
@param: delay_seconds: int
@return:
"""
from resilience_patterns_observability.observability.context import \
    current_span
from resilience_patterns_observability.observability.inmemory_tracing import \
    InMemoryTraceSpan

def before_retry_attempt(attempt:int):
    """

    :param attempt:
    :return:
    """
    parent:current_span = current_span.get()
    if not parent:
        return None

    span_retry:current_span = InMemoryTraceSpan(
        name=f"retry.attempt.{attempt}",
        trace_id=parent.trace_id,
        parent_span_id=parent.span_id,)
    span_retry.start()
    return span_retry

def after_retry_attempt(span:current_span):
    if span:
        span.end()

        



class RetryPolicy:
    """
    class Retry policy
    """

    def __init__(self, max_retries: int, delay_seconds: float) -> None:
        self.max_retries = max_retries
        self.delay_seconds = delay_seconds
