import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('Agg')  # Use a non-GUI backend

class PlotGenerator:
    def __init__(self, image_path):
        if not os.path.exists(image_path.split('/')[1]):
            os.makedirs(image_path.split('/')[1])
        self.image_path = image_path

    def generate_exponential_plot(self, mu, mean_mu, values, n):
        # int(10/mu) + np.log10(mu) in order to have enogh space to represent all data
        # int(10/mu) guarantee that lower values have a correct representation when np.log10(mu) will be 0
        # otherwise if the mu value is higher, np.log10(mu) will be reasonable and int(10/mu) will be zero
        
        time_values = np.linspace(0, int(10/mu) + np.log10(mu), 1000)
        pdf = mu * np.exp(-mu * time_values)

        plt.figure(figsize=(8, 6))
        plt.hist(values,bins=np.linspace(0, int(10/mu)  + np.log10(mu), 30), density=True)
        plt.plot(time_values, pdf, label=f'PDF (mu = {mu:.2f})')

        plt.xlabel('Time (seconds)')
        plt.ylabel('Probability Density')
        plt.title(f'Exponential Distribution with Rate {mu} vs {mean_mu:.2f} with {n} trials')
        plt.legend()
        plt.grid(True)
        plt.savefig(self.image_path)
        plt.close()
