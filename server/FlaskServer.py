import sys
from flask import Flask, jsonify, send_file  # For creating Flask app and handling responses
import os                                    # For file operations (deleting files)
import random                                # For setting random seed
import numpy as np

from server.DelayAnalyzer import DelayAnalyzer
from server.CPUBoundTask import CPUBoundTask
from server.PlotGenerator import PlotGenerator


class FlaskServer:
    '''
        #description of the class
        A Server class that initializes a Flask application and sets up routes.
    '''
    def __init__(self, mu_value: float = 10.0, file_path: str = "./data/csv", image_path: str = "./data/images"):
        # Initialize the Flask application within the class
        self.app = Flask(__name__)

        # Store the mu parameter
        self.mu_value = float(mu_value)

        # Set paths based on mu_value
        extensionFileName = f"_{str(self.mu_value).split('.')[0]}_{str(self.mu_value).split('.')[1]}"
        self.csv_path = f"{file_path}/request_delays{extensionFileName}.csv"
        self.images_path = f"{image_path}/plot{extensionFileName}.png"

        # Store configurations in the Flask app
        self.app.config['MU'] = self.mu_value
        self.app.config['csv_path'] = self.csv_path
        self.app.config['images_path'] = self.images_path

        # Initialize routes
        self.__setup_routes()


    def __setup_routes(self):
        # retrieve mu value from configuration attributes of the app
        mu = self.app.config.get('MU')
        
        # inizialize the delay_analyzer and the plot_generator with file names
        delay_analyzer = DelayAnalyzer(self.app.config['csv_path'])
        plot_generator = PlotGenerator(self.app.config['images_path'])

        @self.app.route('/', methods=['GET'])
        def process_task():
            random.seed(42)
            # Sample the delay time and perform a CPU bound operation, then log the delay in the csv file
            delay = np.random.exponential(1.0 / mu)
            CPUBoundTask.run(delay)
            # end_time = time.time()
            # delay_analyzer.log_delay_to_csv(mu, end_time-start_time)
            delay_analyzer.log_delay_to_csv(mu, delay)
            return jsonify({"message": "Task completed", "duration": delay})

        @self.app.route('/plot/', methods=['GET'])
        def plot():
            # Evaluate the mean mu observed in the csv and generate the empirical distribution plot
            mean_delay, n = delay_analyzer.mean_mu_observed(mu)
            values_observed = delay_analyzer.empirical_distribution(mu)
            plot_generator.generate_exponential_plot(mu, mean_delay, values_observed, n)
            return send_file(self.app.config['images_path'], mimetype='image/png')

        @self.app.route('/reset', methods=['GET'])
        def reset():
            # delete the csv file related to this server (launched with that mu)
            if os.path.isfile(self.app.config['csv_path']):
                os.remove(self.app.config['csv_path'])
            return jsonify({"message": "Reset completed"})


    def run(self):
        # Start the Flask application without multithreading
        print(f"Starting Flask app with mu = {self.mu_value}")
        self.app.run(threaded=False)


if __name__ == '__main__':
    # Example usage: instantiate the Server with a specific mu_value
    if len(sys.argv) != 2:
        print("Usage: python server.py <mu_value>")
        sys.exit(1)

    mu_value = sys.argv[1]
    server = FlaskServer(mu_value)  # Instantiate with the provided mu_value
    server.run()                    # Run the Flask app
