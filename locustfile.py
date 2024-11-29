from csv import writer
from locust import HttpUser, task, events
from numpy import random, mean, std, sqrt

MILLISECONDS_PER_SECOND = 1000

class User(HttpUser):

    @task
    def load_home_page(self):
        self.client.get("/")

    def wait_time(self):
        return random.exponential(1/1)  # change it!


@events.request.add_listener
def on_request_success(request_type, name, response_time, response_length, **kwargs):
    response_times.append(response_time)


response_times = []

@events.quitting.add_listener
def on_locust_quit(environment, **kwargs):
    if response_times:
        avg_response_time = mean(response_times) / MILLISECONDS_PER_SECOND
        confidence_interval = calculate_confidence_interval(response_times)
        write_csv(avg_response_time, confidence_interval)


def calculate_confidence_interval(data):
    n = len(data)
    mean_val = mean(data)
    std_err = std(data) / sqrt(n)
    z_score = 1.96  # Approximate z-score for 95% confidence level
    h = std_err * z_score
    return (mean_val - h) / MILLISECONDS_PER_SECOND, (mean_val + h) / MILLISECONDS_PER_SECOND


def write_csv(avg_response_time: float, confidence_interval: tuple[float, float]) -> None:
    with open("data/metrics.csv", 'a', newline='') as file:
        wr = writer(file)
        wr.writerow([avg_response_time, confidence_interval[0], confidence_interval[1]])
        file.close()