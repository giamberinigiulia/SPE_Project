"""
import time

# Funzione ricorsiva per calcolare il numero di Fibonacci
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Esegui il calcolo per un numero grande per simulare un'operazione CPU-bound
if __name__ == "__main__":
    n = 35  # Un numero più grande richiede molto tempo e CPU per essere calcolato
    start_time = time.time()

    print(f"Fibonacci({n}) = {fibonacci(n)}")

    end_time = time.time()
    print(f"Tempo impiegato: {end_time - start_time} secondi")
"""
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
image_path="plot.png"
# Global variable to store the 'mu' value
mu = None  # This will be initialized via an API call

# File to store the delays
csv_file = 'request_delays.csv'

# Function to log the delay in the CSV file
def log_delay_to_csv(delay):
    # Check if file exists to write headers only once
    file_exists = os.path.isfile(csv_file)
    
    # Open the CSV file in append mode
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # If file does not exist, write the header
        if not file_exists:
            writer.writerow(['timestamp', 'delay'])  # Writing the header
        # Write the current timestamp and delay
        writer.writerow([datetime.now().isoformat(), delay])

# Function to simulate a CPU-bound task
def cpu_bound_task(duration):
    # Perform a CPU-bound task for 'duration' seconds
    end_time = time.time() + duration
    while time.time() < end_time:
        # Simulate heavy CPU task by performing unnecessary calculations
        math.sqrt(12345.6789) * math.sqrt(98765.4321)

def analyze_csv(file_path):
    data = pd.read_csv(file_path)
    mean_delay = data['delay'].mean()
    return mean_delay


def generate_exponential_plot(mu, mean_delay):   
    # Generate a range of time values
    time_values = np.linspace(0, 10, 1000)
    
    # Calculate the probability density function (PDF) of the exponential distribution
    pdf = mu * np.exp(-mu * time_values)
    pdf_mean = mean_delay * np.exp(-mean_delay * time_values)

    # Plot the PDF with the exponential distribution over time 
    # mu and mean_delay are used
    plt.plot(time_values, pdf)
    plt.plot(time_values, pdf_mean)

    plt.xlabel('Time (seconds)')
    plt.ylabel('Probability Density')
    plt.title(f'Exponential Distribution with Rate {mu} vs {mean_delay:.2f}')
    plt.legend([f'PDF (mu = {mu})', f'PDF (mu = {mean_delay:.2f})'])
    plt.savefig(image_path)  # Save the plot to a file
    plt.close()


@app.route('/plot')
def plot(mu = 1.0, file_path = "request_delays.csv"):
    mean_delay = analyze_csv(file_path)  # Get the mean delay
    generate_exponential_plot(mu, mean_delay)  # Generate the plot
    return send_file(image_path, mimetype='image/png')

@app.route('/', methods=['GET'])
def process_task():
    #get the mu parameter from GET request
    mu = float(request.args.get('mu',1.0))
    
    # Generate a delay based on the exponential distribution with rate 'mu'
    delay = np.random.exponential(1.0 / mu)
    
    # Simulate the CPU-bound task for the duration of the 'delay'
    cpu_bound_task(delay)
    
    # Log the delay to the CSV file
    log_delay_to_csv(delay)

    # Return a JSON response indicating the task was completed
    return jsonify({"message": "Task completed", "duration": delay})


@app.route('/reset', methods=['GET'])
def reset():
    # Remove the CSV file if it exists
    if os.path.isfile(csv_file):
        os.remove(csv_file)
    
    #return an http response
    return jsonify({"message": "Reset completed"})

@app.route('/requests', methods=['GET'])
#perform like 10 clients requests
def perform_requests():
    for _ in range(10):
        response = requests.get('http://localhost:5000/')
        print(response.json())
    return jsonify({"message": "10 requests performed"})


if __name__ == '__main__':
    # Start the Flask server
    app.run(debug=True)

