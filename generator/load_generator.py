import requests
import time
import os
from multiprocessing import Process
from numpy import random
from csv import writer


class LoadGenerator:

    def __init__(self, num_clients: int, arrival_rate: float, max_time: int, csv_directory: str, target_url: str | None = None) -> None:
        self.num_clients = num_clients
        self.arrival_rate = arrival_rate
        self.max_time = max_time
        self.target_url = target_url
        self.csv_filename = csv_directory + "/response_times.csv"

        random.seed(10)

        # TODO: remove this operation if it's done in the main both for the generator and the server
        if os.path.exists(self.csv_filename):
            os.remove(self.csv_filename)

    def send_request(self) -> None:
        elapsed_time = 0
        response_times = []

        while elapsed_time < self.max_time:
            start_time = time.time()
            try:
                waiting_time = random.exponential(1/self.arrival_rate)
                time.sleep(waiting_time)
                if self.target_url is None:     # if it's None the generator is used for testing 
                    start_response_time = time.time() 
                    waiting_time = random.exponential(1/8)      # mu = 8 TODO: change it!
                    time.sleep(waiting_time)
                    end_response_time = time.time()
                    response_times.append(end_response_time - start_response_time)
                else:
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

    def __write_csv(self, response_times: list[float]) -> None:
        with open(self.csv_filename, 'a', newline='') as file:
            wr = writer(file)
            wr.writerow(response_times)
            file.close()

    def generate_load(self) -> None:
        processes = []

        for _ in range(self.num_clients):
            process = Process(target=self.send_request)
            processes.append(process)
            process.start()

        for process in processes:
            process.join()
