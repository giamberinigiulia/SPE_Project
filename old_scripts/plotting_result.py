import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create the main for analyzing the csv file (time and delays) and calculate the mean of the delays
def analyze_csv(file_path):
    # Load the data from the CSV file
    data = pd.read_csv(file_path)
    
    # Calculate the mean delay
    mean_delay = data['delay'].mean()
    
    return mean_delay

# plot the graph of the exponential distribution with rate mu

def plot_exponential_distribution(mu, mean_delay):   
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
    plt.show()

# Test the functions

# Path to the CSV file
if __name__ == '__main__':
    mean_delay = analyze_csv('request_delays.csv')
    plot_exponential_distribution(mu, mean_delay)  # Replace 0.5 with the desired rate value

