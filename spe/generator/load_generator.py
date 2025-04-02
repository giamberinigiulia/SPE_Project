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

        join_timeout = self.client_request_time + 30
        end_time = time.time() + self.client_request_time + 60

        # This is needed to avoid memory leaks in the queue, so we read in small chunks
        # otherwise when testing with 300 seconds and 15 clients, the load generator crashes
        while time.time() < end_time and any(p.is_alive() for p in processes):
            try:
                while not queue.empty():
                    response_times.extend(queue.get(block=False))
            except Exception as e:
                print(f"Error reading from queue: {e}")
            time.sleep(1)  # Avoid busy-waiting

        for process in processes:
            process.join(timeout=join_timeout)
            
            if process.is_alive():
                print(f"Process {process.pid} did not terminate in time, forcing termination")
                process.terminate()
                process.join(1)

        while not queue.empty():
            try:
                response_times.extend(queue.get(block=False))
            except Exception as e:
                print(f"Error reading the queue: {e}")
        

        avg_response_time = compute_mean(response_times)
        ci = compute_confidence_intervals(response_times)
        write_csv("data/metrics.csv", avg_response_time, ci[0], ci[1])
       