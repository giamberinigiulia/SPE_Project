import os
import subprocess
import csv
import numpy as np
import scipy.stats as st

import generator.test_generator as tg

MILLISECONDS_PER_SECOND = 1000


def run_locust_test(users):
    # Command to run Locust in headless mode
    command = [
        "locust", "--headless",
        "-u", str(users),
        "-r", str(users),  # Users' spawn rate
        "-t", "20s",  # Test duration
        "-H", "http://127.0.0.1:5000"
    ]

    subprocess.run(command, capture_output=True, text=True)  # maybe remove capture and text


def main():
    if os.path.exists("data/metrics.csv"):
        os.remove("data/metrics.csv")

    user_count_range = range(10, 21)
    theoretical_arts = []
    theoretical_utils = []
    avg_response_times = []
    ci_lower = []
    ci_upper = []

    for users in user_count_range:
        run_locust_test(users)

    for users in user_count_range:
        theoretical_art, theoretical_util = tg.compute_theoretical_metrics(users, 1, 10, 20)
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

    # Calculate confidence intervals for the theoretical ARTs

    # print(f"[DEBUG] Avg response times: {avg_response_times}")
    # print(f"[DEBUG] CI lower: {ci_lower}")
    # print(f"[DEBUG] CI upper: {ci_upper}")

    tg.save_metrics_plot(user_count_range, theoretical_arts, theoretical_utils,
                         avg_response_times, ci_lower, ci_upper, "locust")


if __name__ == "__main__":
    main()
