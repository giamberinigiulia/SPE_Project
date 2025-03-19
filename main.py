import time
from multiprocessing import Process

import requests

from spe.generator import simulation
import spe.argument_parser as arg

TARGET_URL = "http://127.0.0.1:5000"

if __name__ == '__main__':
    parser = arg.create_parser()
    system_config = arg.parse_arguments(parser)

    print(TARGET_URL+ "/mu/" + str(system_config.service_rate))
    response = requests.get(TARGET_URL+ "/mu/" + str(system_config.service_rate))
    print(response.text)
    simulation.start_load_simulation(system_config)

"""
gunicorn -w 4 -b 127.0.0.1:5000 --access-logfile access.log --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(p)s' --error-logfile error.log spe.server.flask_server:app 
gunicorn -w 4 -b 127.0.0.1:5000 --access-logfile access.log --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(p)s %(L)s' --error-logfile error.log spe.server.flask_server:app
"""