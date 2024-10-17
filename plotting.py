import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('Agg')  # Use a non-GUI backend

class PlotGenerator:
    def __init__(self, image_path):
        self.image_path = image_path

    def generate_exponential_plot(self, mu, mean_mu, values):
        time_values = np.linspace(0, int(10 / mu), 1000)
        pdf = mu * np.exp(-mu * time_values)
        # pdf_mean = mean_mu * np.exp(-mean_mu * time_values)


        # plt.hist(bins=num_bins, density=True)
        plt.figure(figsize=(8, 6))
        #plt.plot(time_values, pdf, label=f'PDF (mu = {mu})')
        plt.hist(values,bins=np.linspace(0,int(10/mu),30), density=True)
        plt.plot(time_values, pdf, label=f'PDF (mu = {mu:.2f})')

        plt.xlabel('Time (seconds)')
        plt.ylabel('Probability Density')
        plt.title(f'Exponential Distribution with Rate {mu} vs {mean_mu:.2f}')
        plt.legend()
        plt.grid(True)
        plt.savefig(self.image_path)
        plt.close()
