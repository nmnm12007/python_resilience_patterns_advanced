"""
Calling Service - A - Our Own Service that calls a Downstream Service B
"""

import logging
from typing import Any

import requests
from flask import Flask, jsonify

from resilience_patterns_observability.core.resilience_executor import resilient
from resilience_patterns_observability.policies.bulkhead_policy import BulkheadPolicy
from resilience_patterns_observability.policies.cb_policy import CircuitBreakerPolicy
from resilience_patterns_observability.policies.retry_policy import RetryPolicy
from resilience_patterns_observability.policies.timeout_policy import TimeoutPolicy

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


@resilient(
    RetryPolicy(max_retries=3, delay_seconds=2),
    CircuitBreakerPolicy(failure_threshold=3, recovery_timeout=10),
    BulkheadPolicy(max_concurrent_calls=2, acquire_timeout=5),
    TimeoutPolicy(2),
)
def call_downstream_service_b() -> Any:
    """
    fn that calls the downstream service
    """
    result = requests.get("http://127.0.0.1:5001/call_downstream", timeout=3)
    result.raise_for_status()
    return result.text


@app.route("/api_b")
def api_b() -> Any:
    """
    Function that calls the api endpoint of downstream - service b
    """
    try:
        result = call_downstream_service_b()
        return jsonify({"status": "SUCCESS", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "Failed to call downstream service", "result": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
