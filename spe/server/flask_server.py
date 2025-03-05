import threading
import time
from flask import Flask, jsonify, request, send_file  # For creating Flask app and handling responses
import numpy as np

# from server.delay_analyzer import DelayAnalyzer
from spe.server.cpubound_task import CPUBoundTask
# from server.plot_generator import PlotGenerator

# create a pool of processes
from multiprocessing import Manager, Pool, Process, Queue, Event  # Ensure Queue and Event are imported from multiprocessing

class FlaskServer:
    """
    A server class that simulates an M/M/k queue using Flask.
    """

    def __init__(self, mu_value: float = 10.0, k_servers: int = 1, arrival_rate: float = 1.0):
        """
        Initialize the M/M/k system with a specified arrival rate (lambda), service rate (mu), and number of servers (k).
        :param mu_value: The service rate of the servers (1 / service time).
        :param k_servers: The number of servers in the system.
        :param arrival_rate: The arrival rate of requests (lambda).
        """
        self.app = Flask(__name__)

        self.mu_value = mu_value  # Service rate per server
        self.k_servers = k_servers  # Number of servers
        self.arrival_rate = arrival_rate  # Arrival rate (lambda)

        # Initialize a queue for requests using multiprocessing.Queue
        self.manager = Manager()  # Create a Manager to share objects between processes
        self.queue = Queue()  # Queue for tasks
        self.event_dict = self.manager.dict()  # Dictionary to store Events for each task

        # Initialize Flask routes
        self.__setup_routes()

    def __setup_routes(self):
        """Setup Flask routes."""
        self.app.add_url_rule('/', 'process_task', self.process_task, methods=['GET'])
        self.app.add_url_rule('/end', 'end_server', self.end_server, methods=['GET'])

    def process_task(self):
        """Handle incoming task request and simulate the queuing process."""
        arrival_time = time.time()  # Track when the request arrives
        task_id = str(arrival_time)  # Create a unique task ID based on the arrival time
        task_event = self.manager.Event()  # Create an event for this specific task

        # Add the event to the shared dictionary with the task ID
        self.event_dict[task_id] = task_event

        # Queue the request for later processing
        self.queue.put((task_id, arrival_time))

        # Wait for the task to be completed by a worker
        task_event.wait()  # Wait for this specific task to be completed

        return jsonify({"message": "Task completed"})

    def end_server(self):
        """End the server and provide statistics."""
        server_shutdown_time = time.time()
        print(f"Server started and ended at {server_shutdown_time}")
        return jsonify({
            "message": "Server stopped.",
            "server_shutdown_time": server_shutdown_time
        })

    def worker(self, worker_id: int):
        """Process worker for handling requests."""
        while True:
            if not self.queue.empty():
                # Process the task
                task_id, arrival_time = self.queue.get()
                delay = np.random.exponential(1.0 / self.mu_value)
                print(f"Worker-{worker_id} is processing task with task ID {task_id}, arrival time {arrival_time}, and delay {delay}\n")
                # Simulate the CPU-bound task
                CPUBoundTask.run(delay)

                print(f"Worker-{worker_id} processed task with task ID {task_id}, arrival time {arrival_time}, and delay {delay}\n")
                # Signal that this specific task is completed using the event stored in the shared dict
                self.event_dict[task_id].set()  # Signal that this specific task is completed

    def run(self):
        """Start the Flask application with multiprocessing."""
        print(f"Starting Flask app with mu = {self.mu_value}, k = {self.k_servers}, and arrival rate = {self.arrival_rate}")

        # Create a pool of workers (number of servers)
        workers = [Process(target=self.worker, args=(worker_id,)) for worker_id in range(self.k_servers)]
        for worker in workers:
            worker.start()

        # Start the Flask app without threading
        self.app.run(debug=False, threaded=False)

        # Gracefully shut down workers
        for worker in workers:
            worker.terminate()
            worker.join()  # Ensure each worker terminates properly