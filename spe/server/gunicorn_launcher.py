import os
import subprocess
import time
from spe.argument_parser import Config
from spe.utils.file import delete_file_if_exists

def start_gunicorn(target_url, access_log, error_log, system_config: Config):
    """Deletes old log files and starts Gunicorn with specified parameters."""
    num_servers = system_config.number_of_servers

    # Delete the log files if they exist
    delete_file_if_exists(access_log)
    delete_file_if_exists(error_log)

    # Gunicorn command
    gunicorn_cmd = [
        "gunicorn",
        "-w", str(num_servers),  # Use number_of_servers as workers
        "-b", target_url,  # Bind to the target URL
        "--access-logfile", access_log,
        "--access-logformat", '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(p)s %(L)s',
        "--error-logfile", error_log,
        "spe.server.flask_server:app"  # Adjust this based on your actual Flask app
    ]

    print(f"[INFO] Starting Gunicorn on {target_url} with {num_servers} workers...")

    # Start Gunicorn
    gunicorn_process = subprocess.Popen(gunicorn_cmd)

    # Wait a bit to ensure Gunicorn starts
    time.sleep(2)

    print("[INFO] Gunicorn started successfully!")
    return gunicorn_process
