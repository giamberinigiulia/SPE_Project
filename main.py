import time
from multiprocessing import Process

from spe.generator import load_simulation
import spe.argument_parser as arg
from spe.server.flask_server import FlaskServer

FOLDER_PATH = "./data"
URL = "http://127.0.0.1:5000"


def start_server(mu_value, server_count):
    # Create a Server instance and run it
    server = FlaskServer(mu_value, server_count)
    server.run()


if __name__ == '__main__':
    parser = arg.create_parser()
    service_rate, arrival_rate, user_range, user_request_time, server_count = arg.parse_arguments(parser)

    server = Process(target=start_server, args=[service_rate, server_count])
    server.start()
    time.sleep(2)

    load_simulation.start_load_simulation(user_range, arrival_rate, service_rate, user_request_time, server_count)
    server.join()