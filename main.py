from multiprocessing import Process
import os
import shutil
import subprocess
import sys
import time

from load_generator.generator import LoadGenerator
from server.FlaskServer import FlaskServer

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

    # reset the data folder
    if os.path.exists("./data/csv"):
        shutil.rmtree("./data/csv")
        os.makedirs("./data/csv")
    if os.path.exists("./data/images"):
        shutil.rmtree("./data/images/")
        os.makedirs("./data/images/")

    # retrieve from command line n_client, lambda, maxtime, mu
    print(sys.argv)
    mu = sys.argv[1]
    enter_rate = float(sys.argv[2])
    max_time = int(sys.argv[3])
    client_number = int(sys.argv[4])
    help_message = f"Usage: python main.py <mu> <lambda> <maxtime> <n_client>"
    

    server = Process(target=start_server, args=[mu])
    server.start()
    time.sleep(2)
    

    client = Process(target=start_load_generator, args=[client_number, enter_rate, max_time])
    client.start()

    client.join()
    server.join()

