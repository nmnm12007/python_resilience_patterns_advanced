import yaml

from resilience_full_impl.policy.retry_policy import RetryPolicy
from resilience_full_impl.policy.timeout_policy import TimeoutPolicy


class ResilienceConfigLoader:
    """
        Resilience Config Loader
    """
    def load_config(self, config_path: str):
        """

        :param config_path:
        :return:
        """
        with open(config_path, "r") as f:
            raw_config = yaml.safe_load(f)

        resilience = raw_config.get("resilience", {})
        retry_policy = self._build_retry_config(resilience.get("retry", {}))
        timeout_policy = self._build_timeout_config(
            resilience.get("timeout", {}))

        return {
            "retry":retry_policy,
            "timeout":timeout_policy
        }


    def _build_retry_config(self, cfg: dict) -> RetryPolicy:
        self._validate_retry(cfg)

        return RetryPolicy(
            max_attempts=cfg["max_attempts"],
            retry_interval_ms=cfg["retry_interval_ms"],
            exponential=cfg["exponential"]
        )


    def _build_timeout_config(self, cfg: dict) -> TimeoutPolicy:
        if cfg["timeout_seconds"] <= 0:
            raise ValueError("timeout_seconds must be positive")

        return TimeoutPolicy(timeout_seconds=cfg["timeout_seconds"])

    def _validate_retry(self, cfg: dict) -> None:
        if cfg["max_attempts"] <= 0:
            raise ValueError("max_attempts must be positive")
        if cfg["retry_interval_ms"] <= 0:
            raise ValueError("retry_interval_ms must be positive")
        if not isinstance(cfg["exponential"], bool):
            raise ValueError("exponential must be boolean")