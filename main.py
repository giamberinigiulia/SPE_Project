import time
from multiprocessing import Process

from spe.generator import simulation
import spe.argument_parser as arg
from spe.server.flask_server import FlaskServer

# Maybe is possible to move this class in flask server module
def start_server(system_config: arg.Config) -> None:
    # Create a Server instance and run it
    server = FlaskServer(system_config.service_rate, system_config.number_of_servers)
    server.run()


if __name__ == '__main__':
    parser = arg.create_parser()
    system_config = arg.parse_arguments(parser)

    server = Process(target=start_server, args=[system_config])
    server.start()
    time.sleep(2)

    simulation.start_load_simulation(system_config)
    server.join()
