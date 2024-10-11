import pandas as pd

# Function to calculate the rate of the delays, with a given mu 
def analyze_csv(file_path, mu):
    data = pd.read_csv(file_path)
    filtered_data = data[data['mu'] == mu]
    n = filtered_data.shape[0]
    if not filtered_data.empty:
        mean_delay = filtered_data['delay'].mean()
        return 1/mean_delay, n  # Return the rate (1/mean delay)
    else:
        raise ValueError(f"No data found for mu = {mu}")
