import argparse
import os
import shutil
import time
from multiprocessing import Process
from load_generator.generator import LoadGenerator
from server.FlaskServer import FlaskServer

CSV_FOLDER_PATH = "./data/csv"
IMAGES_FOLDER_PATH = "./data/images"


def start_server(mu_value):
    # Create a Server instance and run it
    server = FlaskServer(mu_value)
    server.run()


def start_load_generator(client_number, enter_rate, max_time, target_url: str = "http://127.0.0.1:5000"):
    # Create a LoadGenerator instance and run it
    lg = LoadGenerator(number_clients=client_number, enter_rate=enter_rate,
                       max_time=max_time, target_url=target_url)
    lg.generate_load()


if __name__ == '__main__':
    # parse the parameters <mu> <lambda> <maxtime> <n_client>
    # Example: python main.py 10 2.5 1000 50
    # Note: the server should be started before running this script, and it should be accessible at http://127.0.0.1:5000

    # py main.py -s <mu> -c <l> <t> <n>

    # py main.py -mu <mu> -lambda <l> -maxtime <t> -nclients <n>

    parser = argparse.ArgumentParser(description="Process some parameters.")

    # Adding arguments to the parser
    parser.add_argument('-mu', type=float, required=True, help='Parameter mu (e.g., rate of arrival)')
    parser.add_argument('-lambda', type=float, required=True, dest='l', help='Parameter lambda (e.g., service rate)')
    parser.add_argument('-maxtime', type=float, required=True, help='Maximum time to run the simulation')
    parser.add_argument('-nclients', type=int, required=True, help='Number of clients to simulate')

    # Parse the arguments
    args = parser.parse_args()

    # reset the data folder
    if os.path.exists(CSV_FOLDER_PATH):
        shutil.rmtree(CSV_FOLDER_PATH)
        os.makedirs(CSV_FOLDER_PATH)
    if os.path.exists(IMAGES_FOLDER_PATH):
        shutil.rmtree(IMAGES_FOLDER_PATH)
        os.makedirs(IMAGES_FOLDER_PATH)
    '''
    # retrieve from command line n_client, lambda, maxtime, mu
    print(sys.argv)
    mu = sys.argv[1]
    enter_rate = float(sys.argv[2])
    max_time = int(sys.argv[3])
    client_number = int(sys.argv[4])
    help_message = f"Usage: python main.py <mu> <lambda> <maxtime> <n_client>"
    
    '''
    server = Process(target=start_server, args=[args.mu])
    server.start()
    time.sleep(2)

    client = Process(target=start_load_generator, args=[args.nclients, args.l, args.maxtime])
    client.start()

    client.join()
    server.join()
