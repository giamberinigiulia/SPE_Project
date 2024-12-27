import spe.generator.load_generator as lg
import spe.utils.file as file
from spe.utils.metrics import compute_theoretical_metrics
from spe.utils.plot import save_metrics_plot

TARGET_URL = "http://127.0.0.1:5000"


def start_load_simulation(user_range: range, arrival_rate: float, service_rate: float, client_request_time: int, server_count: int) -> None:
    print("[DEBUG] start_load_generator called")

    file.delete_file_if_exists(file.CSV_FILENAME)

    theoretical_arts = []
    theoretical_utils = []

    for users in user_range:
        _run_load_simulation(users, arrival_rate, TARGET_URL, client_request_time)
        theoretical_art, theoretical_util = compute_theoretical_metrics(
            users, arrival_rate, service_rate, client_request_time, server_count)
        theoretical_arts.append(theoretical_art)
        theoretical_utils.append(theoretical_util)

    system_metrics = file.read_csv(file.CSV_FILENAME)

    print("[DEBUG] ending simulation")
    file.delete_file_if_exists(file.CSV_FILENAME)
    save_metrics_plot(user_range, theoretical_arts, theoretical_utils, system_metrics, 
                      f"simulation_s{service_rate}_a{arrival_rate}_t{client_request_time}_k{server_count}")


def _run_load_simulation(users: int, arrival_rate: float, target_url: str, client_request_time: int) -> None:
    load_generator = lg.LoadGenerator(users, arrival_rate, target_url, client_request_time)
    load_generator.generate_load()
