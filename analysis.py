import pandas as pd

def analyze_csv(file_path, mu):
    """Analyze the CSV file and return the mean delay for a given mu."""
    data = pd.read_csv(file_path)
    filtered_data = data[data['mu'] == mu]
    
    if not filtered_data.empty:
        mean_delay = filtered_data['delay'].mean()
        return 1 / mean_delay  # Return the rate (1/mean delay)
    else:
        raise ValueError(f"No data found for mu = {mu}")
