''' TODO: module description

'''

import requests
import threading
import time
from numpy import random
from csv import writer
import os


class LoadGenerator:
    ''' TODO: class description

    '''

    def __init__(self, clients_number: int, enter_rate: float, max_time: int, target_url: str) -> None:
        self.clients_number = clients_number
        self.enter_rate = enter_rate
        self.max_time = max_time
        self.target_url = target_url

        self.csv_file_name = 'response_time.csv'

        random.seed(10)

        if os.path.exists(self.csv_file_name):
            os.remove(self.csv_file_name)

    def __send_request(self) -> None:
        passed_time = 0
        response_time = []
        while passed_time < self.max_time:
            start_time = time.time()
            try:
                waiting_time = random.exponential(1/self.enter_rate)
                time.sleep(waiting_time)
                response = requests.get(self.target_url)
                if response.status_code == 200:     # ignore responses with an error
                    response_time.append(response.elapsed.total_seconds())
                print(f"Response: {response.status_code}, Time: {response.elapsed.total_seconds()}")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            end_time = time.time()
            passed_time += (end_time - start_time)
        self.__write_csv(response_time)

    def __write_csv(self, response_time: [float]) -> None:
        with open(self.csv_file_name, 'a') as file:
            wr = writer(file)
            wr.writerow(response_time)
            file.close()

    def generate_load(self) -> None:
        threads = []

        for _ in range(self.clients_number):
            thread = threading.Thread(target=self.__send_request)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
