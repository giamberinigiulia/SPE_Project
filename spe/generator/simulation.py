import spe.generator.load_generator as lg
import spe.utils.file as file
from spe.utils.metric import compute_theoretical_metrics
from spe.utils.plot import save_metrics_plot
from spe.argument_parser import Config
import spe.utils.file as file
import re

def calculate_utilization_from_logs(log_file_path, simulation_duration, num_servers):
    """
    Calculate server utilization from Gunicorn access logs.
    
    Args:
        log_file_path: Path to the access log file
        simulation_duration: Total duration of the simulation in seconds
        num_servers: Number of server workers (c in M/M/c/K)
        
    Returns:
        float: Utilization as a value between 0 and 1
    """
    # Extract request response durations with regex
    pattern = r'.*\[(.*?)\].*" \d+ \d+ <\d+> ([\d.]+)'
    
    request_times = []
    with open(log_file_path, 'r') as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                duration = float(match.group(2))  # Request duration in seconds
                request_times.append(duration)
    
    total_busy_time = sum(request_times)
    max_possible_busy_time = num_servers * simulation_duration    
    utilization = min(1.0, total_busy_time / max_possible_busy_time)
    return utilization


def start_load_simulation(target_url: str, system_config: Config) -> None:
    print("[DEBUG] Simulation started: invoked start_load_simulation")

    arrival_rate = system_config.arrival_rate
    user_range = system_config.user_range
    client_request_time = system_config.user_request_time
    request_time = system_config.user_request_time
    number_of_servers = system_config.number_of_servers
    utilizations = []

    file.delete_file_if_exists(file.CSV_FILENAME)
    theoretical_metrics = compute_theoretical_metrics(system_config)

    for number_of_users in user_range:
        _run_load_simulation(number_of_users, arrival_rate, target_url, client_request_time)
        utilization = calculate_utilization_from_logs("access.log", request_time, number_of_servers)
        utilizations.append(utilization)
        file.truncate_file("access.log")

    print("[DEBUG] Simulation finished: metric's plot generated")
    print(f"Utilizations: {utilizations}")
    system_metrics = file.read_csv(file.CSV_FILENAME)
    file.delete_file_if_exists(file.CSV_FILENAME)

    # TODO: refactor the code of save_metrics_plot
    save_metrics_plot(system_config, theoretical_metrics, system_metrics, utilizations)

def _run_load_simulation(number_of_users: int, arrival_rate: float, target_url: str, client_request_time: int) -> None:
    load_generator = lg.LoadGenerator(number_of_users, arrival_rate, target_url, client_request_time)
    load_generator.generate_load()
