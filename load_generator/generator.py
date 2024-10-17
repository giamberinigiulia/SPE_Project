''' TODO: module description

'''

import requests
import threading
import time
from numpy import random


class LoadGenerator:
    ''' TODO: class description

    '''

    def __init__(self, clients_number: int, enter_rate: float, max_time: int, target_url: str) -> None:
        self.clients_number = clients_number
        self.enter_rate = enter_rate
        self.max_time = max_time
        self.target_url = target_url
        random.seed(10)

    def __send_request(self) -> None:
        passed_time = 0
        while passed_time < self.max_time:
            start_time = time.time()
            try:
                waiting_time = random.exponential(1/self.enter_rate)
                print(waiting_time)
                time.sleep(waiting_time)
                response = requests.get(self.target_url)
                print(f"Response: {response.status_code}, Time: {response.elapsed.total_seconds()}")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            end_time = time.time()
            passed_time += (end_time - start_time)

    def generate_load(self) -> None:
        threads = []

        for _ in range(self.clients_number):
            thread = threading.Thread(target=self.__send_request)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
