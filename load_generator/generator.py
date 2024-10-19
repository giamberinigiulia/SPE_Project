''' TODO: module description

'''
import multiprocessing

import requests
#import threading
from multiprocessing import Process
import time
from numpy import random
from csv import writer
import os


class LoadGenerator:
    ''' TODO: class description

    '''

    csv_file_name = 'response_time.csv'

    def __init__(self, clients_number: int, enter_rate: float, max_time: int, target_url: str) -> None:
        self.clients_number = clients_number
        self.enter_rate = enter_rate
        self.max_time = max_time
        self.target_url = target_url

        random.seed(10)

        if os.path.exists(self.csv_file_name):
            os.remove(self.csv_file_name)

    def send_request(self) -> None:
        passed_time = 0
        response_time = []

        while passed_time < self.max_time:
            start_time = time.time()
            try:
                start_response_time = time.time()
                waiting_time = random.exponential(1/self.enter_rate)
                time.sleep(waiting_time)
                #response = requests.get(self.target_url)
                waiting_time = random.exponential(1/8)
                time.sleep(waiting_time)
                end_request_time = time.time()
                # if response.status_code == 200:     # ignore responses with an error
                #     end_request_time = time.time()
                    #response_time.append(response.elapsed.total_seconds())
                response_time.append(end_request_time - start_response_time)
                # commented only for testing purpouse
                #print(f"Response: {response.status_code}, Time: {response.elapsed.total_seconds()}")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            end_time = time.time()
            passed_time += (end_time - start_time)
        #print(passed_time)
        self.__write_csv(response_time)

    def __write_csv(self, response_time: [float]) -> None:
        with open(self.csv_file_name, 'a', newline='') as file:
            wr = writer(file)
            wr.writerow(response_time)
            file.close()

    def generate_load(self) -> None:
        threads = []

        #multiprocessing.set_start_method('spawn')
        for _ in range(self.clients_number):
            thread = Process(target=self.send_request)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
