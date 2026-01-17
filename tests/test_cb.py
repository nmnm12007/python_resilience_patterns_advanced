from resilience_full_impl.executor.circuit_breaker import CircuitBreaker, \
    CircuitBreakerException
from resilience_full_impl.executor.resilience_executor import \
    ResilienceExecutor
from resilience_full_impl.policy.cb_policy import CircuitBreakerPolicy
from resilience_full_impl.policy.retry_policy import RetryPolicy
from resilience_full_impl.policy.timeout_policy import TimeoutPolicy


def errored_function(token):
    raise RuntimeError("[TEST] : Run Time Error")


if __name__ == "__main__":
    retry = RetryPolicy(max_attempts=3,retry_interval_ms=200, exponential=False)
    timeout = TimeoutPolicy(timeout_seconds=1)
    cb_policy = CircuitBreakerPolicy(failure_threshold=2, recovery_timeout=5)

    cb = CircuitBreaker(cb_policy)

    executor = ResilienceExecutor(retry_policy=retry,cb_policy=cb_policy)

    try:
        executor.execute(errored_function, timeout)
    except Exception as e:
        pass

    try:
        executor.execute(errored_function, timeout)
    except Exception:
        pass

    try:
        executor.execute(errored_function, timeout)
        print("❌ ERROR: circuit should be open")
    except CircuitBreakerException:
        print("✅ Circuit breaker opened correctly")


