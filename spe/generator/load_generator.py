import time
from multiprocessing import Process, Queue

import requests
import numpy as np

from spe.utils.metric import compute_mean, compute_confidence_intervals
from spe.utils.file import write_csv


class LoadGenerator:
    rng = np.random.default_rng(42)

    def __init__(self, client_count: int, arrival_rate: float, target_url: str, client_request_time: int) -> None:
        self.client_count = client_count
        self.arrival_rate = arrival_rate
        self.target_url = target_url
        self.client_request_time = client_request_time

    def send_requests(self, queque: Queue) -> None:
        elapsed_time = 0.0
        response_times = []

        while elapsed_time < self.client_request_time:
            start_time = time.time()
            try:
                time.sleep(self._compute_exponential_time())
                start_response_time = time.time()
                response = requests.get(self.target_url)

                if response.status_code == 200:     # ignore responses with an error
                    end_response_time = time.time()
                    response_times.append(end_response_time - start_response_time)
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

            end_time = time.time()
            elapsed_time += (end_time - start_time)

        queque.put(response_times)

    def _compute_exponential_time(self) -> float:
        return self.rng.exponential(1/self.arrival_rate)

    def generate_load(self) -> None:
        processes = []
        queue = Queue()
        response_times = []

        for _ in range(self.client_count):
            process = Process(target=self.send_requests, args=[queue])
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        while not queue.empty():
            response_times.extend(queue.get())

        avg_response_time = compute_mean(response_times)
        ci = compute_confidence_intervals(response_times)
        write_csv("data/metrics.csv", avg_response_time, ci[0], ci[1])
       