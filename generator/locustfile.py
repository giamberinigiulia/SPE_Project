import time
import numpy as np
from csv import writer
from locust import HttpUser, task, events
from locust.env import Environment
from scipy import stats
from typing import Tuple, List, Any

MILLISECONDS_PER_SECOND = 1000

response_times = []
rng = np.random.default_rng(42)


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--arrival-rate", type=float, env_var="LOCUST_MY_ARGUMENT")


class User(HttpUser):

    @task
    def load_server_page(self):
        with self.client.get("/") as response:
            if response.status_code == 200:
                elapsed_time = response.elapsed.seconds
                think_time = rng.exponential(1/self.environment.parsed_options.arrival_rate)
                time.sleep(think_time)
                response_times.append(elapsed_time + think_time)

   
# @events.request.add_listener
# def on_request_success(response_time, **kwargs: Any):

#     response_times.append(response_time / MILLISECONDS_PER_SECOND + think_time)


@events.quitting.add_listener
def on_locust_quit(environment: Environment, **kwargs: Any) -> None:
    print(f"Quitting Locust and I have arrival rate of: {environment.parsed_options.arrival_rate}")
    if response_times:
        avg_response_time = sum(response_times)/len(response_times)
        ci = compute_confidence_interval(response_times)
        write_csv(avg_response_time, ci[0], ci[1], len(response_times))


def compute_confidence_interval(data: List) -> Tuple[float, float]:
    mean = np.mean(data)
    std = np.std(data)
    n_obs = len(data)
    margin_of_error = (std / np.sqrt(n_obs)) * stats.t.ppf((1 + 0.95) / 2, n_obs - 1)
    return (mean - margin_of_error, mean + margin_of_error)


def write_csv(avg_response_time: float, lower_bound: float, upper_bound: float, number_of_responses: int) -> None:
    with open("data/metrics.csv", 'a', newline='') as file:
        wr = writer(file)
        wr.writerow([avg_response_time, lower_bound, upper_bound, number_of_responses])
        file.close()
