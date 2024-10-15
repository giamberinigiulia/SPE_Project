''' TODO: module description

'''

import requests
import threading
import time
from numpy import random


class LoadGenerator:
    ''' TODO: class description

    '''

    def __init__(self, clients_number: int, enter_rate: float, request_number: int,  target_url: str) -> None:
        self.clients_number = clients_number
        self.enter_rate = enter_rate
        self.num_request = request_number
        self.target_url = target_url

    def __send_request(self) -> None:
        try:
            waiting_time = random.exponential(1/self.enter_rate)
            time.sleep(waiting_time)
            response = requests.get(self.target_url)
            print(f"Response: {response.status_code}, Time: {response.elapsed.total_seconds()}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def generate_load(self) -> None:
        threads = []

        for _ in range(self.num_request):
            if len(threads) >= self.clients_number:
                for thread in threads:
                    thread.join()
                threads = []

            thread = threading.Thread(target=self.__send_request)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
