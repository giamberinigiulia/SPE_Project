import json

def generate_json(mu_rate: float, lambda_rate: float, number_clients: int, max_time: int, data_folder: str):

    config = {
        "mu_rate": mu_rate,
        "lambda_rate": lambda_rate,
        "number_clients": number_clients,
        "max_time": max_time
    }
    with open(data_folder + '/config.json', 'w') as f:
        json.dump(config, f)
    

def read_json(json_path: str):

    with open(json_path, 'r') as f:
        config = json.load(f)
        if config: 
            mu_rate = config.get("mu_rate")
            lambda_rate = config.get("lambda_rate")
            number_clients = config.get("number_clients")
            max_time = config.get("max_time")

    return mu_rate, lambda_rate, number_clients, max_time