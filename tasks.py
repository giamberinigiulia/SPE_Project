import os
import csv
import math
import time

csv_file = 'request_delays.csv'

def log_delay_to_csv(mu, delay):
    """Log the delay into a CSV file."""
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

def cpu_bound_task(duration):
    """Simulate a CPU-bound task."""
    end_time = time.time() + duration
    while time.time() < end_time:
        # Simulate heavy CPU task by performing unnecessary calculations
        math.sqrt(12345.6789) * math.sqrt(98765.4321)
