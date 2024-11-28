import argparse
import os
import shutil
import time
import datetime
from multiprocessing import Process

import json_config_manager as manager
import generator.test_generator as tg
from server.flask_server import FlaskServer

FOLDER_PATH = "./data"
URL = "http://127.0.0.1:5000"


def start_server(mu_value, file_path, images_path):
    # Create a Server instance and run it
    server = FlaskServer(mu_value, file_path, images_path)
    server.run()


# TODO: add parameter to specify the folder for the CSV
def start_load_generator(client_count, arrival_rate, service_rate, max_time):
   # Test for the average response time
    theoretical_arts, measured_arts, theoretical_utils = tg.get_average_response_times(
        client_count, arrival_rate, service_rate, max_time)
    tg.plot_art(client_count, theoretical_arts, measured_arts, theoretical_utils)


if __name__ == '__main__':
    # Note: the server should be started before running this script, and it should be accessible at http://127.0.0.1:5000

    parser = argparse.ArgumentParser(description="Process some parameters.")

    # Define two subcommands, "Values Parser" to pass values ​​manually through main.py v -m <mu> -l <lambda> -t <maxtime> -n <nclients>
    # and "Json Parser" to pass values ​​through json file through argument -c.
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Configuration "Values Parser": main.py v -m <mu> -l <lambda> -t <maxtime> -n <nclients>
    arguments_parser = subparsers.add_parser(
        "v", help="Values Parser mode: main.py v -m <mu> -l <lambda> -t <maxtime> -n <nclients>")
    arguments_parser.add_argument('-m', type=float, required=True,
                                  help='Parameter mu (e.g., rate of arrival)')
    arguments_parser.add_argument('-l', type=float, required=True,
                                  help='Parameter lambda (e.g., service rate)')
    arguments_parser.add_argument('-t', type=int, required=True,
                                  help='Maximum time to run the simulation')
    arguments_parser.add_argument('-n', type=int, required=True,
                                  help='Number of clients to simulate')

    # Configuration "Json Parser": main.py j -c <json_file_path>
    json_parser = subparsers.add_parser("j", help="Json Parser mode: main.py j -c <json_file_path>")
    json_parser.add_argument("-c", type=str, required=True, help="Path of confi.json file")

    args = parser.parse_args()

    # Checking the selected mode
    if args.mode == "v":
        mu_rate = args.m
        lambda_rate = args.l
        client_count = args.n
        max_time = args.t

    elif args.mode == "j":
        mu_rate, lambda_rate, client_count, max_time = manager.read_json(args.c)

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

    manager.generate_json(mu_rate, lambda_rate, client_count, max_time, data_folder)

    server = Process(target=start_server, args=[mu_rate, data_folder_csv, data_folder_images])
    server.start()
    time.sleep(2)

    client = Process(target=start_load_generator, args=[
                  client_count, lambda_rate, mu_rate, max_time])
    client.start()

    client.join()
    server.join()
