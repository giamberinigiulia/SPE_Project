"""Module for generating HTTP load on a target server using parallel clients."""
import time
from multiprocessing import Process, Queue
from typing import List, Tuple

import requests
import numpy as np

from spe.utils.metric import compute_mean, compute_confidence_intervals


class LoadGenerator:
    """
    Generates HTTP load on a target server using multiple parallel client processes.

    This class simulates multiple independent clients making requests to a server with
    exponentially distributed inter-arrival times, collects response times,
    and calculates statistics.
    """
    rng = np.random.default_rng(42)

    def __init__(self, client_count: int, arrival_rate: float, target_url: str, client_request_time: int) -> None:
        self.client_count = client_count
        self.arrival_rate = arrival_rate
        self.target_url = target_url
        self.client_request_time = client_request_time

    def generate_load(self) -> Tuple[float, float, float]:
        """
        Run load test with multiple client processes and collect statistics.

        Returns:
            Tuple containing:
            - Average response time (float)
            - Lower bound of confidence interval (float)
            - Upper bound of confidence interval (float)
        """
        processes = []
        queue = Queue()
        response_times = []

        processes = self._start_client_processes(queue)
        response_times = self._collect_response_times(queue, processes)
        avg_response_time = compute_mean(response_times)
        ci_lower, ci_upper = compute_confidence_intervals(response_times)
        return avg_response_time, ci_lower, ci_upper

    def _start_client_processes(self, queue: Queue) -> List[Process]:
        processes = []

        for _ in range(self.client_count):
            process = Process(target=self._send_requests, args=[queue])
            processes.append(process)
            process.start()

        return processes

    def _send_requests(self, queque: Queue) -> None:
        """
        Send HTTP requests to the target URL with exponentially distributed intervals.

        Args:
            queue: Queue to which response times will be added
        """
        response_times = []
        elapsed_time = 0.0

        while elapsed_time < self.client_request_time:
            start_time = time.time()
            try:
                time.sleep(self.rng.exponential(1/self.arrival_rate))
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

    def _collect_response_times(self, queue: Queue, processes: List[Process]) -> List[float]:
        """
        Collect response times from queue and clean up processes.

        Args:
            queue: Queue containing response time lists from client processes
            processes: List of client processes

        Returns:
            List of response times collected from all processes
        """
        response_times = []
        join_timeout = self.client_request_time + 30

        # Periodically collect results to avoid memory issues
        # that happened with many clients and long client request times
        end_time = time.time() + self.client_request_time + 60
        while time.time() < end_time and any(p.is_alive() for p in processes):
            self._drain_queue(queue, response_times)
            time.sleep(1)  # Avoid busy waiting

        for process in processes:
            process.join(timeout=join_timeout)
            if process.is_alive():
                print(f"Process {process.pid} did not terminate, terminating forcefully")
                process.terminate()
                process.join(1)

        self._drain_queue(queue, response_times)
        return response_times

    def _drain_queue(self, queue: Queue, response_times: List[float]) -> None:
        """Empty the queue and extend response_times list."""
        try:
            while not queue.empty():
                response_times.extend(queue.get(block=False))
        except Exception as e:
            print(f"Error reading from queue: {e}")
