import requests
import time
import os
from multiprocessing import Process
from numpy import random
from csv import writer


class LoadGenerator:
    ''' TODO: class description

    '''

    csv_filename = './data/csv/response_time.csv'

    def __init__(self, number_clients: int, enter_rate: float, max_time: int, target_url: str) -> None:
        self.clients_number = number_clients
        self.enter_rate = enter_rate
        self.max_time = max_time
        self.target_url = target_url

        random.seed(10)

        if os.path.exists(self.csv_filename):
            os.remove(self.csv_filename)

    def send_request(self) -> None:
        passed_time = 0
        response_time = []

        while passed_time < self.max_time:
            start_time = time.time()
            try:
                start_response_time = time.time()
                waiting_time = random.exponential(1/self.enter_rate)
                time.sleep(waiting_time)
                response = requests.get(self.target_url)
                #waiting_time = random.exponential(1/8)
                #time.sleep(waiting_time)
                end_request_time = time.time()
                if response.status_code == 200:     # ignore responses with an error
                    end_request_time = time.time()
                    response_time.append(end_request_time - start_response_time)
                # commented only for testing purpouse
                # print(f"Response: {response.status_code}, Time: {response.elapsed.total_seconds()}")
            # TODO: handle exception
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            end_time = time.time()
            passed_time += (end_time - start_time)
        # print(passed_time)
        self.__write_csv(response_time)

    def __write_csv(self, response_time: list[float]) -> None:
        with open(self.csv_filename, 'a', newline='') as file:
            wr = writer(file)
            wr.writerow(response_time)
            file.close()

    def generate_load(self) -> None:
        threads = []

        for _ in range(self.clients_number):
            thread = Process(target=self.send_request)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
