from resilience_full_impl.config.loader import ResilienceConfigLoader
from pathlib import Path


def main():
    loader = ResilienceConfigLoader()
    project_root = Path(__file__).resolve().parents[1]
    config_path = (project_root / "src" / "resilience_full_impl" / "config" /
                   "defaults.yaml")
    policies = loader.load_config(str(config_path))

    retry_policy = policies["retry"]
    timeout_policy = policies["timeout"]

    print("RetryPolicy loaded", retry_policy)
    print("TimeoutPolicy loaded", timeout_policy)


if __name__ == "__main__":
    main()
