"""
Execution Context
"""
from resilience_full_impl.cancellation.cancellation_token import \
    CancellationToken
from resilience_full_impl.policy.retry_policy import RetryPolicy
from resilience_full_impl.policy.timeout_policy import TimeoutPolicy


class ExecutionContext:
    """
         ExecutionContext
    """
    def __init__(self, retry_pol: RetryPolicy, timeout_pol: TimeoutPolicy,
                 token: CancellationToken):
        self.retry_pol = retry_pol
        self.timeout_pol = timeout_pol
        self.token = token


