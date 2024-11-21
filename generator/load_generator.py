import requests
import time
import os
from multiprocessing import Process
from numpy import random
from csv import writer


class LoadGenerator:

    def __init__(self, client_count: int, arrival_rate: float, target_url: str, client_request_time: int, csv_directory: str) -> None:
        self.client_count = client_count
        self.arrival_rate = arrival_rate
        self.target_url = target_url
        self.client_request_time = client_request_time
        self.csv_filename = csv_directory + "/response_times.csv"

        random.seed(10)

        if os.path.exists(self.csv_filename):
            os.remove(self.csv_filename)

    def send_requests(self) -> None:
        elapsed_time = 0
        response_times = []

        while elapsed_time < self.client_request_time:
            start_time = time.time()
            try:
                waiting_time = random.exponential(1/self.arrival_rate)
                time.sleep(waiting_time)
                start_response_time = time.time()
                response = requests.get(self.target_url)
                if response.status_code == 200:     # ignore responses with an error
                    end_response_time = time.time()
                    response_times.append(end_response_time - start_response_time)
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            end_time = time.time()
            elapsed_time += (end_time - start_time)

        self.__write_csv(response_times)

    def __write_csv(self, response_times: list) -> None:
        with open(self.csv_filename, 'a', newline='') as file:
            wr = writer(file)
            wr.writerow(response_times)
            file.close()

    def generate_load(self) -> None:
        processes = []

        for _ in range(self.client_count):
            process = Process(target=self.send_requests)
            processes.append(process)
            process.start()

        for process in processes:
            process.join()
