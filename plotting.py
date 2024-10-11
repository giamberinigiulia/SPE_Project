import matplotlib
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Use a non-GUI backend

# Function to generate and save an exponential distribution plot
def generate_exponential_plot(mu, mean_mu, image_path):

    # Generate a range of time values
    time_values = np.linspace(0, int(10/mu), 1000) # changed the right extreme of the interval for lower value of mu
    # Calculate the probability density function (PDF) of the exponential distribution
    pdf = mu * np.exp(-mu * time_values)
    pdf_mean = mean_mu * np.exp(-mean_mu * time_values)

    # Plot the PDF with the exponential distribution over time
    plt.figure(figsize=(8, 6))
    plt.plot(time_values, pdf, label=f'PDF (mu = {mu})')
    plt.plot(time_values, pdf_mean, label=f'PDF (mean_mu = {mean_mu:.2f})')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Probability Density')
    plt.title(f'Exponential Distribution with Rate {mu} vs {mean_mu:.2f}')
    plt.legend()
    plt.grid(True)
    plt.savefig(image_path)  # Save the plot to a file
    plt.close()
