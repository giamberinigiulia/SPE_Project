import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('Agg')  # Use a non-GUI backend


class PlotGenerator:
    def __init__(self, image_path):
        self.file_path = image_path

    def generate_exponential_plot(self, mu, mean_mu, values, n):
        # Calculate time values for the plot
        time_values = np.linspace(0, int(10/mu) + np.log10(mu), 1000)
        # Calculate the probability density function (PDF) for the exponential distribution
        pdf = mu * np.exp(-mu * time_values)

        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.hist(values, bins=np.linspace(0, int(10/mu) + np.log10(mu), 30), density=True)
        plt.plot(time_values, pdf, label=f'PDF (mu = {mu:.2f})')

        # Add labels, title, legend, and grid to the plot
        plt.xlabel('Time (seconds)')
        plt.ylabel('Probability Density')
        plt.title(f'Exponential Distribution with Rate {mu} vs {mean_mu:.2f} with {n} trials')
        plt.legend()
        plt.grid(True)

        # Save the plot to the specified file path and close the plot
        plt.savefig(self.file_path)
        plt.close()
