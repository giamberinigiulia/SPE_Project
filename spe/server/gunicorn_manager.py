"""
Gunicorn Server Launcher Script.

This script performs the following tasks:
1. Deletes old log files (if they exist) to ensure fresh logging.
2. Configures and launches a Gunicorn server instance with the specified parameters.
3. Provides a function to terminate the Gunicorn server process gracefully.

Modules Used:
- `subprocess`: Executes the Gunicorn server as a subprocess.
- `time`: Introduces delays to ensure proper server startup.
- `spe.argument_parser`: Provides the `Config` class for system-level configurations.
- `spe.utils.file`: Contains utility functions for file operations.

Functions:
- `start_gunicorn`: Deletes old log files and starts the Gunicorn server.
- `end_gunicorn`: Terminates the Gunicorn server process.

Parameters:
- `target_url`: The URL to bind the Gunicorn server to (e.g., "127.0.0.1:5000").
- `access_log`: Path to the access log file.
- `error_log`: Path to the error log file.
- `system_config`: An instance of the `Config` class containing system-level configurations, including the number of servers.

Usage:
Call the `start_gunicorn` function with the required parameters to launch the Gunicorn server.

Notes:
- Ensure that the `spe.server.flask_server:app` reference matches the actual location of your Flask application.
- This script assumes that Gunicorn is installed and available in the system's PATH.
"""

import subprocess
import time

from spe.argument_parser import Config
from spe.utils.file import delete_file_if_exists


def start_gunicorn(target_url, access_log, error_log, system_config: Config) -> None:
    """
    Removes old log files and starts a Gunicorn server with the specified configuration, 
    including target URL, log paths, and worker processes.
    """

    num_servers = system_config.number_of_servers

    delete_file_if_exists(access_log)
    delete_file_if_exists(error_log)
    gunicorn_cmd = [
        "gunicorn",
        "-w", str(num_servers),  # Set the number of worker processes
        "-b", target_url,  # Bind Gunicorn to the specified target URL
        "--access-logfile", access_log,
        "--access-logformat", '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(p)s %(L)s',
        "--error-logfile", error_log,
        "spe.server.flask_server:app"  # Reference to the Flask application
    ]

    print(f"[INFO] Starting Gunicorn on {target_url} with {num_servers} workers...")
    process = subprocess.Popen(gunicorn_cmd)
    time.sleep(2)  # This sleep is needed to ensure Gunicorn starts correctly
    print("[INFO] Gunicorn started successfully!")
    return process


def end_gunicorn(process: subprocess.Popen) -> None:
    """
    Terminates the Gunicorn server process.

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
