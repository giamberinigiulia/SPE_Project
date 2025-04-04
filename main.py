"""
SPE Project Simulation Main Script.

This script executes the following steps:
1. Parses command-line arguments to configure the system settings.
2. Launches a Gunicorn server to host the Flask application.
3. Sends an HTTP request to configure the server's service rate.
4. Initiates a load simulation to evaluate server performance.
5. Terminates the Gunicorn server after the simulation completes.

Modules Used:
- `time`: Introduces delays during execution.
- `requests`: Sends HTTP requests to interact with the server.
- `spe.generator.simulation`: Manages the load simulation logic.
- `spe.argument_parser`: Provides tools for parsing command-line arguments.
- `spe.server.gunicorn_launcher`: Handles Gunicorn server initialization and termination.

Constants:
- `PROTOCOL`: Defines the HTTP protocol (default: "http://").
- `TARGET_HOST`: Specifies the server's host and port.
- `ACCESS_LOG`: Path to Gunicorn's access log file.
- `ERROR_LOG`: Path to Gunicorn's error log file.

Usage:
Execute this script with the required command-line arguments to configure the system and run the simulation.

Example:
    python main.py -s 10 -a 5 -u 1 10 -t 60 -k 1
"""

import time
import requests

from spe.generator import simulation
import spe.argument_parser as arg
from spe.server import gunicorn_manager

PROTOCOL = "http://"
TARGET_HOST = "127.0.0.1:5000"
ACCESS_LOG = "access.log"
ERROR_LOG = "error.log"


def configure_service_rate(service_rate: float) -> None:
    response = requests.get(f"{PROTOCOL + TARGET_HOST}/mu/{service_rate}")

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to set service rate. Status code: {response.status_code}, Response: {response.text}"
        )


if __name__ == '__main__':
    print("[INFO] Simulation launched at:", time.strftime("%H:%M:%S", time.localtime()))
    parser = arg.create_parser()
    system_config = arg.parse_arguments(parser)
    # the try-finally block is used to ensure that the Gunicorn processes are terminated even if an error occurs
    try:
        gunicorn_process = gunicorn_manager.start_gunicorn(TARGET_HOST, ACCESS_LOG, ERROR_LOG, system_config)
        configure_service_rate(system_config.service_rate)
        simulation.start_load_simulation(PROTOCOL + TARGET_HOST, system_config)
    finally:
        gunicorn_manager.end_gunicorn(gunicorn_process)
    print("[INFO] Simulation ended at:", time.strftime("%H:%M:%S", time.localtime()))
