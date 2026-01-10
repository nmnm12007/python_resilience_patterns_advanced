"""
Distributed Tracing
"""


import contextvars

current_trace_id = contextvars.ContextVar("current_trace_id", default=None)
current_span = contextvars.ContextVar("current_span", default=None)

