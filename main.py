import os
import shutil
import time
import datetime
from multiprocessing import Process


import locust_main
import argument_parser as arg
from server.flask_server import FlaskServer

FOLDER_PATH = "./data"
URL = "http://127.0.0.1:5000"


def start_server(mu_value, server_count):
    # Create a Server instance and run it
    server = FlaskServer(mu_value, server_count)
    server.run()


if __name__ == '__main__':
    parser = arg.create_parser()
    service_rate, arrival_rate, user_range, user_request_time, server_count = arg.parse_arguments(parser)

    # Create data folder based on current date and time
    '''current_time = datetime.datetime.now()
    dt = current_time.strftime('%Y%m%d') + '_' + current_time.strftime('%H%M%S')

    data_folder = FOLDER_PATH + "/" + dt
    data_folder_csv = data_folder + "/csv"
    data_folder_images = data_folder + "/images"

    # Reset the data folder if already exists
    if os.path.exists(data_folder):
        shutil.rmtree(data_folder)
    os.makedirs(data_folder)
    os.makedirs(data_folder_csv)
    os.makedirs(data_folder_images)'''

    # manager.generate_json(service_rate, arrival_rate, user_range, user_request_time, data_folder)

    # server = Process(target=start_server, args=[service_rate, data_folder_csv, data_folder_images, server_count])
    server = Process(target=start_server, args=[service_rate, server_count])
    server.start()
    time.sleep(2)

    locust_main.start_load_generator(user_range, arrival_rate, service_rate, user_request_time, server_count)
    server.join()