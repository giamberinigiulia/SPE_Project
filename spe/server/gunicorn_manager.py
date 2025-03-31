"""
Gunicorn Server Launcher Script.

This script performs the following tasks:
1. Deletes old log files (if they exist) to ensure fresh logging.
2. Configures and launches a Gunicorn server instance with the specified parameters.

Modules Used:
- `subprocess`: Executes the Gunicorn server as a subprocess.
- `time`: Introduces delays to ensure proper server startup.
- `spe.argument_parser`: Provides the `Config` class for system-level configurations.
- `spe.utils.file`: Contains utility functions for file operations.

Functions:
- `start_gunicorn`: Deletes old log files and starts the Gunicorn server.

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
    num_servers = system_config.number_of_servers  # Number of worker processes for handling requests

    # Delete the log files if they exist
    delete_file_if_exists(access_log) 
    delete_file_if_exists(error_log) 

    # Gunicorn command
    gunicorn_cmd = [
        "gunicorn",
        "-w", str(num_servers),  # Set the number of worker processes
        "-b", target_url,  # Bind Gunicorn to the specified target URL
        "--access-logfile", access_log,  # Specify the access log file path
        "--access-logformat", '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(p)s %(L)s',  # Log format for access logs
        "--error-logfile", error_log,  # Specify the error log file path
        "spe.server.flask_server:app"  # Reference to the Flask application
    ]

    print(f"[INFO] Starting Gunicorn on {target_url} with {num_servers} workers...")

    # Start Gunicorn as a subprocess
    subprocess.Popen(gunicorn_cmd) 

    # Wait a bit to ensure Gunicorn starts
    time.sleep(2)

    print("[INFO] Gunicorn started successfully!")


def end_gunicorn() -> None:
    """
    Terminates the Gunicorn server process.
    """
    try:
        subprocess.run(["killall", "gunicorn"], check=True)
    except subprocess.CalledProcessError:
        pass