import time
from flask import Flask, jsonify
import numpy as np
from spe.server.cpubound_task import CPUBoundTask
from multiprocessing import Pool, Queue
import os
from queue import Full

def execute_task(args):
    """Execute task in worker process"""
    arrival_time, delay = args
    worker_id = os.getpid()

    # Execute the CPU-bound task
    CPUBoundTask.run(delay)
    completion_time = time.time()
    
    return worker_id, completion_time

class FlaskServer:
    def __init__(self, mu_value: float = 10.0, k_servers: int = 1, arrival_rate: float = 1.0):
        self.app = Flask(__name__)
        self.mu_value = mu_value
        self.k_servers = k_servers
        self.arrival_rate = arrival_rate
        # Create a fixed pool of k workers
        self.pool = Pool(processes=k_servers)
        self.request_queue = Queue()
        self.__setup_routes()

    def __setup_routes(self):
        self.app.add_url_rule('/', 'process_task', self.process_task, methods=['GET'])
        self.app.add_url_rule('/end', 'end_server', self.end_server, methods=['GET'])

    def process_task(self):
        """Handle incoming task request and queue if workers are busy"""
        arrival_time = time.time()
        delay = np.random.exponential(1.0 / self.mu_value)
        
        try:
            # Try to queue the request
            self.request_queue.put((arrival_time, delay), timeout=5.0)
            
            # Submit task to worker pool
            result = self.pool.apply_async(
                execute_task,  # Use the global function instead of class method
                args=[(arrival_time, delay)]
            )
            
            # Wait for task completion and get results
            worker_id, completion_time = result.get()
            waiting_time = completion_time - arrival_time
            
            # Remove request from queue after completion
            self.request_queue.get()
            #write in a file with worker_id 
            '''f = open(f"{worker_id}.txt", "a")
            f.write(f"Task completed by Worker {worker_id}\n")
            f.close()'''

            return jsonify({
                "status": "completed",
                "worker_id": worker_id,
                "arrival_time": arrival_time,
                "completion_time": completion_time,
                "waiting_time": waiting_time,
                "expected_delay": delay
            })
            
        except Full:
            print(f"[ERROR] Request queue full, rejecting request\n")
            return jsonify({
                "status": "rejected",
                "error": "Server queue full"
            }), 503
        
        except Exception as e:
            print(f"[ERROR] Task processing failed: {str(e)}\n")
            return jsonify({
                "status": "failed",
                "error": str(e)
            }), 500
            
    def end_server(self):
        """End the server and clean up workers"""
        self.pool.close()
        self.pool.join()
        server_shutdown_time = time.time()
        print(f"[SERVER] Server shutdown at {server_shutdown_time:.4f}")
        return jsonify({
            "message": "Server stopped",
            "server_shutdown_time": server_shutdown_time
        })

    def run(self):
        """Start the Flask application"""
        print(f"Starting Flask app with mu={self.mu_value} and {self.k_servers} servants")
        # Run Flask without processes to use our worker pool
        self.app.run(host="127.0.0.1", port=5000, debug=False, threaded=False)