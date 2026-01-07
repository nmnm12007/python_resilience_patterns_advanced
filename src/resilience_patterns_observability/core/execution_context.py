"""
    Define the Execution Context for retry, cb, bk
ExecutionContext
====================
├─ request_id (correlation)
├─ attempt (retry counter)
├─ start_time (latency tracking)
├─ last_exception (failure reason)
"""

import time
import uuid


class ExecutionContext:
    """
    Execution Context for retry, cb, bk
    class holds the values of unique request ID,
    timestamp of the request, attempt number, last_exception
    """

    from typing import Optional
    
    def __init__(self) -> None:
        self.req_id = str(uuid.uuid4())
        self.timestamp : float= time.time()
        self.attempt = 0
        self.last_exception = None
