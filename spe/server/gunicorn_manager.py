"""This module contains functions to manage the Gunicorn HTTP server."""

import subprocess
import time

import requests

from spe.argument_parser import Config
from spe.utils.file import delete_file_if_exists


def start_gunicorn(target_url: str, access_log: str, error_log: str, system_config: Config) -> subprocess.Popen:
    """
    Starts a Gunicorn server with the specified configuration for the M/M/c queue simulation.

    This function:
    1. Removes any existing log files to ensure clean output
    2. Creates a Gunicorn server with the number of workers specified in system_config
    3. Configures logging to the specified files with detailed access logs

    Args:
        target_url: The URL where the Gunicorn server will listen (e.g., "127.0.0.1:5000")
        access_log: Filepath where access logs will be written
        error_log: Filepath where error logs will be written
        system_config: Configuration object containing simulation parameters,
                      including the number of server workers

    Returns:
        subprocess.Popen: A process object representing the running Gunicorn server,
                        which should be terminated using end_gunicorn()

    Notes:
        This function assumes that Gunicorn is installed and available in the PATH
    """
    num_servers = system_config.number_of_servers

    delete_file_if_exists(access_log)
    delete_file_if_exists(error_log)
    gunicorn_cmd = [
        "gunicorn",
        "-w", str(num_servers),
        "-b", target_url,  # Bind Gunicorn to the specified target URL
        "--access-logfile", access_log,
        "--access-logformat", '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(p)s %(L)s',
        "--error-logfile", error_log,
        "spe.server.flask_server:app"
    ]

    print(f"[INFO] Starting Gunicorn on {target_url} with {num_servers} workers...")
    process = subprocess.Popen(gunicorn_cmd)
    time.sleep(2)  # This sleep is needed to ensure Gunicorn starts correctly
    print("[INFO] Gunicorn started successfully!")
    return process


def end_gunicorn(process: subprocess.Popen) -> None:
    """
    Terminates the Gunicorn server process in a graceful manner.

    Args:
        process: The subprocess.Popen object representing the Gunicorn process
    """
    if process is not None:
        print("[INFO] Stopping Gunicorn server...")
        try:
            process.terminate()
            process.wait(timeout=5)
            print("[INFO] Gunicorn stopped successfully")
        except subprocess.TimeoutExpired:
            print("[WARN] Gunicorn termination timed out, forcing shutdown...")
            process.kill()
        except Exception as e:
            print(f"[ERROR] Error stopping Gunicorn: {e}")


def configure_service_rate(host: str, service_rate: float) -> None:
    """Send a request to the server to set the service rate (μ)."""
    response = requests.get(f"{host}/mu/{service_rate}")

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to set service rate. Status code: {response.status_code}, Response: {response.text}"
        )
