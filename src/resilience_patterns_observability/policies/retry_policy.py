"""
define retry policy
@param: max_retries: int
@param: delay_seconds: int
@return:
"""


class RetryPolicy:
    """
    class Retry policy
    """

    def __init__(self, max_retries:int, delay_seconds:float) -> None:
        self.max_retries = max_retries
        self.delay_seconds = delay_seconds
