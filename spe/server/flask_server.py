import time
from flask import Flask, jsonify, request, send_file  # For creating Flask app and handling responses
import numpy as np

# from server.delay_analyzer import DelayAnalyzer
from spe.server.cpubound_task import CPUBoundTask
# from server.plot_generator import PlotGenerator

# create a pool of processes
from multiprocessing import Pool


class FlaskServer:
    '''
        #description of the class
        A Server class that initializes a Flask application and sets up routes.
    '''

    # attributes for logging the server inactivity state and evaluate the overall inactivity time
    server_starting_time = 0 # initialized before launching the server
    server_active_time = 0 # counter time for activity periods
    first_call = True
    _pool = None


    def __init__(self, mu_value: float = 10.0, server_count: int = 1):

        self.app = Flask(__name__)

        self.k_server = server_count
        self._pool = Pool(processes = self.k_server)
        self.mu_value = float(mu_value)
        self.rng = np.random.default_rng(42)     

        self.__setup_routes()


    def __setup_routes(self):
        @self.app.route('/', methods=['GET'])
        def process_task():
            
            if self.first_call:
                # Initialize the server starting time
                self.server_starting_time = time.time()
                print(f"Starting time: {self.server_starting_time}")
                self.first_call = False

            delay = self.rng.exponential(1.0 / self.mu_value)
            execution_time = self._pool.map(CPUBoundTask.run, [delay])
            self.server_active_time += execution_time[0]

            return jsonify({"message": "Task completed"})

        @self.app.route('/end', methods=['GET'])
        def end_server():
            # Log the server shutdown time
            server_shutdown_time = time.time()
            # Print the server duration time 
            print(f"Server started at {self.server_starting_time} and ended at {server_shutdown_time}")
            print(f"Server duration: {server_shutdown_time - self.server_starting_time} seconds")
            print(f"Server active time: {self.server_active_time} seconds")
            print(f"Server activity utils: {(self.server_active_time * self.k_server / (server_shutdown_time - self.server_starting_time)) * 100} %")
            # Return JSON response with calculated metrics
            return jsonify({
                "activity_period": self.server_active_time,
                "server_up_time": server_shutdown_time - self.server_starting_time,
                "measured_utils_percentage": (self.server_active_time / (server_shutdown_time - self.server_starting_time)) * 100
                })
            # (self.server_active_time/k) / (server_shutdown_time - self.server_starting_time)) * 100
            # s1: 2s/10s, s2: 3s/10s, s3: 4s/10s --> 9s/(10s * 3) --> 30% --> 0.3
            # s1: 2s/10s, s2: 3s/10s, s3: 4s/10s --> (9s / 3)/10s --> 30% --> 0.3

        # @self.app.route('/refresh', methods=['GET']) --> chiamata bloccante --> il load generator non invia load finchè non riceve risposta
        # altrimenti non siamo in grado di valutare le metriche e rilanciare il tutto --> salvare in un csv (?)
        # salvarsi quante richieste sono state accolte e per ogni richiesta il numero di server attualmente in funzione 
        # calcolare il tempo di attività di ogni server e il tempo di inattività
        @self.app.route('/refresh', methods=['GET'])
        def refresh_server():

            return jsonify({"message": "Server is refreshing"})
            

    def run(self):
        # Start the Flask application without multithreading
        print(f"Starting Flask app with mu = {self.mu_value}")
        self.app.run(debug=False,threaded=False)

    