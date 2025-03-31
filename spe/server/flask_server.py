"""
SPE Project Flask Server.

This script implements a Flask-based server that performs the following tasks:
1. Handles HTTP requests to process CPU-bound tasks with an exponential delay.
2. Allows dynamic configuration of the service rate (`mu`) via a REST API.
3. Provides an endpoint to terminate the server gracefully.

Modules Used:
- `os`: Handles file operations and process management.
- `signal`: Sends signals to terminate the server process.
- `json`: Reads and writes JSON data for storing the service rate.
- `flask`: Provides the web framework for handling HTTP requests.
- `numpy`: Generates random numbers for simulating task delays.
- `spe.server.cpubound_task`: Executes CPU-bound tasks.

Constants:
- `MU_FILE`: Path to the file where the service rate (`mu`) is stored.

Endpoints:
1. `/` (GET): Processes a CPU-bound task with a delay sampled from an exponential distribution.
2. `/mu/<mu_value>` (GET): Updates the service rate (`mu`) dynamically.
3. `/end` (GET): Terminates the server process.
"""

import os
import signal
import json
import subprocess
from flask import Flask, jsonify
import numpy as np
import psutil

from spe.server.cpubound_task import CPUBoundTask

app = Flask(__name__)

# Path to the file where the shared 'mu' value will be stored
MU_FILE = '/tmp/mu_value.json'

# Initialize the value of mu from the file (if exists) or set it to default (1.0)
def load_mu():
    """
    Load the service rate (`mu`) from the file if it exists, otherwise return the default value (1.0).
    """
    if os.path.exists(MU_FILE):
        with open(MU_FILE, 'r') as f:
            return json.load(f).get('mu', 1.0)
    return 1.0

# Store the value of mu in the file
def store_mu(mu_value):
    """
    Store the service rate (`mu`) in the file for persistence.
    """
    with open(MU_FILE, 'w') as f:
        json.dump({"mu": mu_value}, f)

# Shared random number generator
rng = np.random.default_rng(42)

@app.route('/', methods=['GET'])
def process_task():
    """
    Process a CPU-bound task with a delay sampled from an exponential distribution.
    The delay is inversely proportional to the service rate (`mu`).
    """
    # Read 'mu' from the file
    mu = load_mu()
    delay = rng.exponential(1 / mu)
    print(f"[DEBUG] Delay sampled: {delay} \t mu: {mu}")
    
    # Execute the CPU-bound task with the sampled delay
    CPUBoundTask.run(delay)

    return jsonify({"message": "Task completed", "duration": delay})

@app.route('/mu/<mu_value>', methods=['GET'])
def get_service_rate(mu_value):
    """
    Update the service rate (`mu`) dynamically via the URL parameter.
    The new value is stored in the file for persistence.
    """
    # Convert the URL parameter to a float and update 'mu'
    mu_value = float(mu_value)
    store_mu(mu_value)
    print(f"[INFO] Updated mu: {mu_value}")

    return jsonify({"message": f"Service rate updated successfully (mu: {mu_value})"})

@app.route('/end', methods=['GET'])
def end_server():
    """
    Terminate the server process gracefully by sending a SIGINT signal.
    """
    os.kill(os.getppid(), signal.SIGINT)
    return jsonify({"message": "Server ended"})

if __name__ == '__main__':
    app.run(debug=True)