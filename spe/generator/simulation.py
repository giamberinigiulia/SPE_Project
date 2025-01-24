import spe.generator.load_generator as lg
import spe.utils.file as file
from spe.utils.metric import compute_theoretical_metrics
from spe.utils.plot import save_metrics_plot
from spe.argument_parser import Config
#
import requests
#
TARGET_URL = "http://127.0.0.1:5000"


def start_load_simulation(system_config: Config) -> None:
    print("[DEBUG] start_load_generator called")

    arrival_rate = system_config.arrival_rate
    user_range = system_config.user_range
    client_request_time = system_config.user_request_time

    file.delete_file_if_exists(file.CSV_FILENAME)
    theoretical_metrics = compute_theoretical_metrics(system_config)

    for number_of_users in user_range:
        _run_load_simulation(number_of_users, arrival_rate, TARGET_URL, client_request_time)

    system_metrics = file.read_csv(file.CSV_FILENAME)
    file.delete_file_if_exists(file.CSV_FILENAME)
    save_metrics_plot(system_config, theoretical_metrics, system_metrics)
    print("[DEBUG] end of simulation!")

    response = None
    while response is None or response.status_code != 200:
        response = requests.get(TARGET_URL + "/end")
        print("[DEBUG SERVER -> SIMULATION] Response from the server: {response.text}")

def _run_load_simulation(number_of_users: int, arrival_rate: float, target_url: str, client_request_time: int) -> None:
    # from now on, it will be executed with number_of_users
    load_generator = lg.LoadGenerator(number_of_users, arrival_rate, target_url, client_request_time)
    load_generator.refresh_server(number_of_users)
    load_generator.generate_load()
    load_generator.get_server_status()  # Get server status after each simulation
