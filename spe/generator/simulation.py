"""This module is responsible for simulating load on a web server."""
import spe.utils.file as file
from spe.generator.load_generator import LoadGenerator
from spe.utils.argument_parser import Config
from spe.utils.metric import MeasuredMetric, compute_theoretical_metrics, compute_utilization_from_logs
from spe.utils.plot import save_metrics_plot


def run_load_simulation(target_url: str, system_config: Config) -> None:
    """
    Run a complete load simulation across a range of user counts.
    This function collect the metrics in a CSV file and generates a plot comparing theoretical and measured metrics.

    Args:
        target_url: The URL to target with the load test
        system_config: Configuration parameters for the simulation
    """
    file.delete_file_if_exists(file.CSV_PATH)
    theoretical_metrics = compute_theoretical_metrics(system_config)

    for number_of_users in system_config.user_range:
        _collect_measured_metrics(target_url, number_of_users, system_config)

    system_metrics = file.read_metrics_from_csv(file.CSV_PATH)
    save_metrics_plot(system_config, theoretical_metrics, system_metrics)
    print("[INFO] Simulation finished: metrics' plot generated successfully")


def _collect_measured_metrics(target_url: str, number_of_users: int, system_config: Config) -> None:
    """
    Execute a single load test with specified parameters and collect performance metrics.

    Args:
        target_url: The URL to target with the load test
        number_of_users: Number of simulated users for this test
        system_config: Configuration parameters for the simulation
    """
    arrival_rate = system_config.arrival_rate
    user_request_time = system_config.user_request_time
    number_of_servers = system_config.number_of_servers

    load_generator = LoadGenerator(number_of_users, arrival_rate, target_url, user_request_time)
    avg_time, ci_lower, ci_upper = load_generator.generate_load()
    utilization = compute_utilization_from_logs(
        "access.log", user_request_time, number_of_servers)
    file.truncate_file("access.log")
    file.write_metrics_to_csv(file.CSV_PATH, MeasuredMetric(
        avg_time, ci_lower, ci_upper, utilization))
