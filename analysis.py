import csv
import numpy as np
import pandas as pd
import os

class DelayAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path

    def mean_mu_observed(self, mu):
        data = pd.read_csv(self.file_path)
        filtered_data = data[data['mu'] == mu]
        n = filtered_data.shape[0]
        if not filtered_data.empty:
            mean_delay = filtered_data['delay'].mean() 
            return 1 / mean_delay, n  # Return the rate (1/mean delay)
        else:
            raise ValueError(f"No data found for mu = {mu}")

    def empirical_distribution(self,mu):
        data = pd.read_csv(self.file_path)
        filtered_data = data[data['mu'] == mu]
        return filtered_data['delay']
    
    def log_delay_to_csv(self, mu, delay):
        """Log the delay into a CSV file."""
        file_exists = os.path.isfile(self.file_path)

        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['mu', 'delay'])  # Writing the header
            writer.writerow([mu, delay])
