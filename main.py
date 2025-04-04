"""Main script for running the simulation of an M/M/c queue system."""

import time

from spe.generator import simulation
import spe.argument_parser as arg
from spe.server import gunicorn_manager as manager

PROTOCOL = "http://"
TARGET_HOST = "127.0.0.1:5000"
ACCESS_LOG = "access.log"
ERROR_LOG = "error.log"


def main() -> None:
    """
    Execute the M/M/c queue simulation workflow.

    This function:
    1. Parses command line arguments to configure the simulation
    2. Starts a Gunicorn server with the specified configuration
    3. Configures the service rate for request processing
    4. Launches the load simulation against the target endpoint
    5. Ensures the Gunicorn server is properly terminated after simulation
    """
    print("[INFO] Simulation launched at:", time.strftime("%H:%M:%S", time.localtime()))
    parser = arg.create_parser()
    system_config = arg.parse_arguments(parser)
    # the try-finally block is used to ensure that the Gunicorn processes are terminated even if an error occurs
    try:
        gunicorn_process = manager.start_gunicorn(TARGET_HOST, ACCESS_LOG, ERROR_LOG, system_config)
        manager.configure_service_rate(PROTOCOL + TARGET_HOST, system_config.service_rate)
        simulation.start_load_simulation(PROTOCOL + TARGET_HOST, system_config)
    finally:
        manager.end_gunicorn(gunicorn_process)
    print("[INFO] Simulation ended at:", time.strftime("%H:%M:%S", time.localtime()))


if __name__ == '__main__':
    main()
