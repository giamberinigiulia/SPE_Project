from csv import writer
from locust import HttpUser, task, events
from numpy import random, mean
import numpy as np
from scipy import stats

MILLISECONDS_PER_SECOND = 1000

response_times = []


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--arrival-rate", type=float, env_var="LOCUST_MY_ARGUMENT")


class User(HttpUser):

    @task
    def load_home_page(self):
        self.client.get("/")

    def wait_time(self):
        return random.exponential(1/self.environment.parsed_options.arrival_rate)


@events.request.add_listener
def on_request_success(request_type, name, response_time, response_length, **kwargs):
    response_times.append(response_time / MILLISECONDS_PER_SECOND)


@events.quitting.add_listener
def on_locust_quit(environment, **kwargs):
    print(f"Quitting Locust and I have arrival rate of: {environment.parsed_options.arrival_rate}")
    if response_times:
        avg_response_time = mean(response_times)
        ci = confidence_interval(response_times)
        write_csv(avg_response_time, ci[0], ci[1])


def confidence_interval(data):
    mean = np.mean(data)
    std = np.std(data)
    n_obs = len(data)
    margin_of_error = (std / np.sqrt(n_obs)) * stats.t.ppf((1 + 0.95) / 2, n_obs - 1)
    return (mean - margin_of_error, mean + margin_of_error)


def write_csv(avg_response_time: float, lower_bound: float, upper_bound: float) -> None:
    with open("data/metrics.csv", 'a', newline='') as file:
        wr = writer(file)
        wr.writerow([avg_response_time, lower_bound, upper_bound])
        file.close()
