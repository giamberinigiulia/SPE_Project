import os
import subprocess
import csv
import scipy.stats as st

import generator.test_generator as tg

MILLISECONDS_PER_SECOND = 1000


def run_locust_test(users: int, arrival_rate: float, client_request_time: int) -> None:
    # Command to run Locust in headless mode
    command = [
        "locust", 
        "--arrival-rate", str(arrival_rate),
        "--headless",
        "-u", str(users),
        "-r", str(users),  # Users' spawn rate
        "-t", f"{client_request_time}s",  # Test duration
        "-H", "http://127.0.0.1:5000",
    ]

    subprocess.run(command, capture_output=True, text=True)


def start_load_generator(user_range: range, arrival_rate: float, service_rate: float, client_request_time: int) -> None:
    if os.path.exists("data/metrics.csv"):
        os.remove("data/metrics.csv")

    theoretical_arts = []
    theoretical_utils = []
    avg_response_times = []
    ci_lower = []
    ci_upper = []

    for users in user_range:
        run_locust_test(users, arrival_rate, client_request_time)

    for users in user_range:
        theoretical_art, theoretical_util = tg.compute_theoretical_metrics(users, arrival_rate, service_rate, client_request_time)
        theoretical_arts.append(theoretical_art)
        theoretical_utils.append(theoretical_util)
        print(f"[DEBUG] Computed theoretical util {theoretical_util} for {users} clients.")

    for art in theoretical_arts:
        lower, upper = st.t.interval(confidence=0.95, df=len(
            theoretical_arts)-1, loc=art, scale=st.sem(theoretical_arts))
        ci_lower.append(lower)
        ci_upper.append(upper)

    with open("data/metrics.csv", 'r', newline='') as response_time_csv:
        csv_reader = csv.reader(response_time_csv)
        for metrics in csv_reader:
            avg_response_times.append(float(metrics[0]))

    tg.save_metrics_plot(user_range, theoretical_arts, theoretical_utils,
                         avg_response_times, ci_lower, ci_upper, "locust")

