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
