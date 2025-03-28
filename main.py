import requests
import json

from spe.generator import simulation
import spe.argument_parser as arg
from spe.server import gunicorn_launcher

PROTOCOL = "http://"
TARGET_HOST = "127.0.0.1:5000"
ACCESS_LOG = "access.log"
ERROR_LOG = "error.log"

if __name__ == '__main__':
    # Parse arguments from system_config
    parser = arg.create_parser()
    system_config = arg.parse_arguments(parser)

    # Start Gunicorn
    gunicorn_launcher.start_gunicorn(TARGET_HOST, ACCESS_LOG, ERROR_LOG, system_config)

    # Continue with the rest of the script
    response = requests.get(f"{PROTOCOL + TARGET_HOST}/mu/{system_config.service_rate}")
    response_data = json.loads(response.text)
    print(f"[DEBUG] {response_data['message']}")

    simulation.start_load_simulation(PROTOCOL + TARGET_HOST, system_config)

"""
gunicorn -w 4 -b 127.0.0.1:5000 --access-logfile access.log --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(p)s' --error-logfile error.log spe.server.flask_server:app 
gunicorn -w 4 -b 127.0.0.1:5000 --access-logfile access.log --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(p)s %(L)s' --error-logfile error.log spe.server.flask_server:app
"""