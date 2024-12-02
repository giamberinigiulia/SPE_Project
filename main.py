import argparse
import os
import shutil
import time
import datetime
from multiprocessing import Process

import json_config_manager as manager
import generator.test_generator as tg
import locust_main
from server.flask_server import FlaskServer

FOLDER_PATH = "./data"
URL = "http://127.0.0.1:5000"


def start_server(mu_value, file_path, images_path):
    # Create a Server instance and run it
    server = FlaskServer(mu_value, file_path, images_path)
    server.run()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process some parameters.")

    subparsers = parser.add_subparsers(dest="mode", required=True)

    arguments_parser = subparsers.add_parser(
        "v", help="Values Parser mode: main.py v -m <mu> -l <lambda> -t <maxtime> -n <nclients>")
    arguments_parser.add_argument('-s', type=float, required=True,
                                  help='Parameter service rate')
    arguments_parser.add_argument('-a', type=float, required=True,
                                  help='Parameter arrival rate')
    arguments_parser.add_argument('-t', type=int, required=True,
                                  help='Maximum time to run the simulation')
    arguments_parser.add_argument('-u', type=int, nargs=2, required=True,
                                  help='Range of users')

    # Configuration "Json Parser": main.py j -c <json_file_path>
    json_parser = subparsers.add_parser("j", help="Json Parser mode: main.py j -c <json_file_path>")
    json_parser.add_argument("-c", type=str, required=True, help="Path of confi.json file")

    args = parser.parse_args()

    # Checking the selected mode
    if args.mode == "v":
        service_rate = args.s
        arrival_rate = args.a
        user_range = range(args.u[0], args.u[1] + 1)
        user_request_time = args.t

    elif args.mode == "j":
        service_rate, arrival_rate, user_range, user_request_time = manager.read_json(args.c)

    # Create data folder based on current date and time
    current_time = datetime.datetime.now()
    dt = current_time.strftime('%Y%m%d') + '_' + current_time.strftime('%H%M%S')

    data_folder = FOLDER_PATH + "/" + dt
    data_folder_csv = data_folder + "/csv"
    data_folder_images = data_folder + "/images"

    # Reset the data folder if already exists
    if os.path.exists(data_folder):
        shutil.rmtree(data_folder)
    os.makedirs(data_folder)
    os.makedirs(data_folder_csv)
    os.makedirs(data_folder_images)

    # manager.generate_json(service_rate, arrival_rate, user_range, user_request_time, data_folder)

    server = Process(target=start_server, args=[service_rate, data_folder_csv, data_folder_images])
    server.start()
    time.sleep(2)

    locust_main.start_load_generator(user_range, arrival_rate, service_rate, user_request_time)
    server.join()
