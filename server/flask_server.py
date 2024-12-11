import sys
import time
from flask import Flask, jsonify, request, send_file  # For creating Flask app and handling responses
import os                                    # For file operations (deleting files)
import random                                # For setting random seed
import numpy as np

# from server.delay_analyzer import DelayAnalyzer
from server.cpubound_task import CPUBoundTask
# from server.plot_generator import PlotGenerator
  

class FlaskServer:
    '''
        #description of the class
        A Server class that initializes a Flask application and sets up routes.
    '''

    # attributes for logging the server inactivity state and evaluate the overall inactivity time
    server_starting_time = 0 # initialized before launching the server
    server_active_time = 0 # counter time for activity periods
    first_call = True


    # def __init__(self, mu_value: float = 10.0, file_path: str = "./data/csv", image_path: str = "./data/images", server_count: int = 1):
    def __init__(self, mu_value: float = 10.0, server_count: int = 1):
        # Initialize the Flask application within the class
        self.app = Flask(__name__)

        self.k_server = server_count

        # Store the mu parameter
        self.mu_value = float(mu_value)

        # Set paths based on mu_value
        # extensionFileName = f"_{str(self.mu_value).split('.')[0]}_{str(self.mu_value).split('.')[1]}"
        # self.csv_path = f"{file_path}/request_delays{extensionFileName}.csv"
        # self.images_path = f"{image_path}/plot{extensionFileName}.png"

        # Store configurations in the Flask app
        self.app.config['MU'] = self.mu_value
        # self.app.config['csv_path'] = self.csv_path
        # self.app.config['images_path'] = self.images_path

        # Initialize routes
        self.__setup_routes()

    def __setup_routes(self):
        # retrieve mu value from configuration attributes of the app
        mu = self.app.config.get('MU')

        # inizialize the delay_analyzer and the plot_generator with file names
        # delay_analyzer = DelayAnalyzer(self.app.config['csv_path'])
        # plot_generator = PlotGenerator(self.app.config['images_path'])

        @self.app.route('/', methods=['GET'])
        def process_task():
            
            if self.first_call:
                # Initialize the server starting time
                self.server_starting_time = time.time()
                print(f"Starting time: {self.server_starting_time}")
                self.first_call = False
            
            start_processing = time.time() # update the inactive time by counting from the last active period
            random.seed(42)
            # Sample the delay time and perform a CPU bound operation, then log the delay in the csv file
            delay = np.random.exponential(1.0 / mu)
            CPUBoundTask.run(delay)
            # end_time = time.time()
            # delay_analyzer.log_delay_to_csv(mu, end_time-start_time)
            # delay_analyzer.log_delay_to_csv(mu, delay)
            self.server_active_time += time.time() - start_processing
            return jsonify({"message": "Task completed", "duration": delay})

        @self.app.route('/end', methods=['GET'])
        def end_server():
            # Log the server shutdown time
            server_shutdown_time = time.time()
            # Print the server duration time 
            print(f"Server started at {self.server_starting_time} and ended at {server_shutdown_time}")
            print(f"Server duration: {server_shutdown_time - self.server_starting_time} seconds")
            print(f"Server active time: {self.server_active_time} seconds")
            print(f"Server activity utils: {self.server_active_time * 100 / (server_shutdown_time - self.server_starting_time)} %")
            # Return JSON response with calculated metrics
            return jsonify({
                "activity_period": self.server_active_time,
                "server_up_time": server_shutdown_time - self.server_starting_time,
                "measured_utils_percentage": (self.server_active_time / (server_shutdown_time - self.server_starting_time)) * 100
                })


    def run(self):
        # Start the Flask application without multithreading
        print(f"Starting Flask app with mu = {self.mu_value}")
        self.app.run(threaded=False, processes = self.k_server)
        