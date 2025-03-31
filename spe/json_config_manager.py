"""
JSON Configuration Manager.

This module provides utility functions to generate and read JSON configuration files 
for the SPE Project. These configurations are used to define system parameters 
such as service rates, number of clients, and simulation duration.

Functions:
- `generate_json(mu_rate, lambda_rate, number_clients, max_time, data_folder)`: 
  Creates a JSON configuration file with the specified parameters.
- `read_json(json_path)`: Reads a JSON configuration file and extracts the parameters.

Modules Used:
- `json`: Handles JSON file operations.

Usage:
Import this module to generate or read configuration files for the simulation.

Example:
    from spe.json_config_manager import generate_json, read_json

    # Generate a configuration file
    generate_json(0.5, 1.0, 100, 60, "./data")

    # Read a configuration file
    mu_rate, lambda_rate, number_clients, max_time = read_json("./data/config.json")
"""
import json

def generate_json(mu_rate: float, lambda_rate: float, number_clients: int, max_time: int, data_folder: str) -> None:

    config = {
        "mu_rate": mu_rate,
        "lambda_rate": lambda_rate,
        "number_clients": number_clients,
        "max_time": max_time
    }
    with open(data_folder + '/config.json', 'w') as f:
        json.dump(config, f)


def read_json(json_path: str) -> tuple[float, float, int]:

    with open(json_path, 'r') as f:
        config = json.load(f)
        if config:
            mu_rate = config.get("mu_rate")
            lambda_rate = config.get("lambda_rate")
            number_clients = config.get("number_clients")
            max_time = config.get("max_time")

    return mu_rate, lambda_rate, number_clients, max_time
