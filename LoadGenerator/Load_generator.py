import requests
import threading
import time
from numpy import random


class LoadGenerator:

    def __init__(self, N, enter_rate, num_request, target_url):
        self.N = N
        self.enter_rate = enter_rate
        self.num_request = num_request
        self.target_url = target_url

    def __send_request(self):
        try:
            waiting_time = random.exponential(1/self.enter_rate)
            time.sleep(waiting_time)
            response = requests.get(self.target_url)
            print(f"Response: {response.status_code}, Time: {response.elapsed.total_seconds()}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def generate_load(self):
        threads = []

        for _ in range(self.num_request):
            if len(threads) >= self.N:
                for thread in threads:
                    thread.join()
                threads = []

            thread = threading.Thread(target=self.__send_request)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
