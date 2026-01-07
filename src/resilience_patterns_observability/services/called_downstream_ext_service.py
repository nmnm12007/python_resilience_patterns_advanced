"""
Handle response from the downstream service b
"""

import time
from random import random

from flask import Flask

app = Flask(__name__)


@app.route("/call_downstream", methods=["GET"])
def unstable_service() -> str:
    """
    fn that simulates an unstable downstream service
    """
    time.sleep(2)  # simulate slow dependency

    if random() <= 0.6:
        raise RuntimeError("Downstream failure")

    return "DOWNSTREAM OK"


if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
