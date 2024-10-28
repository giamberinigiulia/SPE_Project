import os
import shutil
import subprocess
import time

from load_generator.generator import LoadGenerator
from server.app import start_server
from multiprocessing import Process

CSV_PATH = "./data/csv"
IMAGES_PATH = "./data/images"

if __name__ == '__main__':
    # parse the parameters <mu> <lambda> <maxtime> <n_client>
    # Example: python main.py 10 2.5 1000 50
    # Note: the server should be started before running this script, and it should be accessible at http://127.0.0.1:5000

    # py main.py -s <mu> -c <l> <t> <n>
    # py main.py -mu <mu> -lambda <l> -maxtime <t> -nclients <n>

    # reset the data folder
    # if os.path.exists("./data/csv"):
    #     shutil.rmtree("./data/csv")
    #     os.makedirs("./data/csv")
    # if os.path.exists("./data/images"):
    #     shutil.rmtree("./data/images/")
    #     os.makedirs("./data/images/")

    # retrieve from command line n_client, lambda, maxtime, mu
    # print(sys.argv)
    # mu = sys.argv[1]
    # enter_rate = float(sys.argv[2])
    # max_time = int(sys.argv[3])
    # client_number = int(sys.argv[4])
    # help_message = f"Usage: python main.py <mu> <lambda> <maxtime> <n_client>"
    
    # subprocess.Popen([sys.executable, './server/app.py', str(mu)])
    # time.sleep(2)
    # lg = LoadGenerator(number_clients=client_number, enter_rate=enter_rate,
    #                        max_time=max_time, target_url="http://127.0.0.1:5000")
    # lg.generate_load()

    if not os.path.exists(CSV_PATH):
        os.makedirs(CSV_PATH)
    
    if not os.path.exists(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)
    
    server = Process(target=start_server)
    server.start()
    time.sleep(1)
    
    lg = LoadGenerator(number_clients=2, enter_rate=4.0,
                           max_time=10, target_url="http://127.0.0.1:5000")
    lg.generate_load()

    server.join()

    
    