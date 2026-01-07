"""
class to check and hold Timeout Policy
"""


class TimeoutPolicy:
    """
         Timeout Policy
    """
    def __init__(self, timeout_seconds: float) -> None:
        self.timeout_seconds = timeout_seconds
