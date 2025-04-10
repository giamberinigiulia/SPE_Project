"""This module implements a Flask-based server for processing CPU-bound tasks with an exponential delay.

Endpoints:
1. `/` (GET): Processes a CPU-bound task with a delay sampled from an exponential distribution.
2. `/mu/<service_rate>` (GET): Updates the service rate (`mu`) dynamically.
"""

import os
import json

import numpy as np
from flask import Flask, jsonify, Response

from spe.server.cpubound_task import CPUBoundTask


MU_FILE_PATH = '/tmp/mu_value.json'  # this is needed to persist the mu value across multiple runs

app = Flask(__name__)
rng = np.random.default_rng(42)


@app.route('/', methods=['GET'])
def process_task() -> Response:
    """
    Load the service rate mu and use it for processing a CPU-bound task. 
    This simulates the server's thinking time of the M/M/k queue.
    """
    mu = _load_service_rate()
    delay = rng.exponential(1 / mu)
    print(f"[DEBUG] Delay sampled: {delay} \t mu: {mu}")
    CPUBoundTask.run(delay)
    return jsonify({"message": "Task completed", "duration": delay})


@app.route('/mu/<service_rate>', methods=['GET'])
def get_service_rate(service_rate: str) -> Response:
    """
    Update the service rate (`mu`) dynamically via the URL parameter.
    The new value is stored in the file for persistence.
    """
    service_rate = float(service_rate)
    _store_service_rate(service_rate)
    print(f"[INFO] Updated mu: {service_rate}")
    return jsonify({"message": f"Service rate updated successfully (mu: {service_rate})"})


def _load_service_rate() -> float:
    """
    Load the service rate (`mu`) from the file if it exists, otherwise return the default value (1.0).
    """
    if os.path.exists(MU_FILE_PATH):
        with open(MU_FILE_PATH, 'r') as f:
            return json.load(f).get('mu', 1.0)
    return 1.0


def _store_service_rate(service_rate: float) -> None:
    """
    Store the service rate (`mu`) in the file for persistence.
    """
    with open(MU_FILE_PATH, 'w') as f:
        json.dump({"mu": service_rate}, f)


if __name__ == '__main__':
    app.run(debug=False)
