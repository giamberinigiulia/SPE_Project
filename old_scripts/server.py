from flask import Flask, request, jsonify, send_file
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import math
import csv
import os
from datetime import datetime
import requests

app = Flask(__name__)

# Image path
image_path="plot.png"
# File to store the delays
csv_file = 'request_delays.csv'
# Global variable to store the 'mu' value
file_path = "request_delays.csv"


# Function to log the delay in the CSV file
def log_delay_to_csv(mu,delay):
    # Check if file exists to write headers only once
    file_exists = os.path.isfile(csv_file)
    
    # Open the CSV file in append mode
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # If file does not exist, write the header
        if not file_exists:
            writer.writerow(['mu', 'delay'])  # Writing the header
        # Write the current timestamp and delay
        writer.writerow([mu, delay])

# Function to simulate a CPU-bound task
def cpu_bound_task(duration):
    # Perform a CPU-bound task for 'duration' seconds
    end_time = time.time() + duration
    while time.time() < end_time:
        # Simulate heavy CPU task by performing unnecessary calculations
        math.sqrt(12345.6789) * math.sqrt(98765.4321)

# Function that evaluate the mean of the real delays
def analyze_csv(file_path, mu): 
    data = pd.read_csv(file_path)
    filtered_data = data[data['mu'] == mu]
    mean_delay = filtered_data['delay'].mean()
    return 1/mean_delay


def generate_exponential_plot(mu, mean_mu):   
    # Generate a range of time values
    time_values = np.linspace(0, 10, 1000)
    
    # Calculate the probability density function (PDF) of the exponential distribution
    pdf = mu * np.exp(-mu * time_values)
    pdf_mean = mean_mu * np.exp(-mean_mu * time_values)

    # Plot the PDF with the exponential distribution over time 
    # mu and mean_mu are used
    plt.plot(time_values, pdf)
    plt.plot(time_values, pdf_mean)

    plt.xlabel('Time (seconds)')
    plt.ylabel('Probability Density')
    plt.title(f'Exponential Distribution with Rate {mu} vs {mean_mu:.2f}')
    plt.legend([f'PDF (mu = {mu})', f'PDF (mu = {mean_mu:.2f})'])
    plt.savefig(image_path)  # Save the plot to a file
    plt.close()


@app.route('/plot', methods=['GET'])
def plot():
    mu = float(request.args.get('mu', 1.0)) # 1.0 is the default value
    mean_delay = analyze_csv(file_path, mu)  # Get the mean delay
    generate_exponential_plot(mu, mean_delay)  # Generate the plot
    return send_file(image_path, mimetype='image/png') # return the image plot

@app.route('/', methods=['GET'])
def process_task():
    #get the mu parameter from GET request
    mu = float(request.args.get('mu', 1.0)) # 1.0 is the default value
    
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
    if os.path.isfile(csv_file):
        os.remove(csv_file)
    
    #return an http response
    return jsonify({"message": "Reset completed"})

if __name__ == '__main__':
    # Start the Flask server
    app.run(debug=True)

