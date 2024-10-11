from flask import request, jsonify, send_file
import numpy as np
from tasks import cpu_bound_task, log_delay_to_csv
from analysis import analyze_csv
from plotting import generate_exponential_plot
import os

image_path = "plot.png"  # Path for saving the plot image

def setup_routes(app):
    @app.route('/plot', methods=['GET'])
    def plot():
        mu = float(request.args.get('mu', 1.0))  # Default mu value
        mean_delay = analyze_csv("request_delays.csv", mu)  # Get the mean delay
        generate_exponential_plot(mu, mean_delay, image_path)  # Generate the plot
        return send_file(image_path, mimetype='image/png')  # Return the image plot

    @app.route('/', methods=['GET'])
    def process_task():
        mu = float(request.args.get('mu', 1.0))  # Default mu value
        
        # Generate a delay based on the exponential distribution with rate 'mu'
        delay = np.random.exponential(1.0 / mu)
        
        # Simulate the CPU-bound task for the duration of the 'delay'
        cpu_bound_task(delay)
        
        # Log the delay to the CSV file
        log_delay_to_csv(mu, delay)

        # Return a JSON response indicating the task was completed
        return jsonify({"message": "Task completed", "duration": delay})

    @app.route('/reset', methods=['GET'])
    def reset():
        # Remove the CSV file if it exists
        if os.path.isfile("request_delays.csv"):
            os.remove("request_delays.csv")
        
        # Return an HTTP response
        return jsonify({"message": "Reset completed"})
