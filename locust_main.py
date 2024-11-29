import os
import subprocess
import csv

import generator.test_generator as tg


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
    theoretical_arts = []
    theoretical_utils = []
    avg_response_times = []
    ci_lower = []
    ci_upper = []

    if os.path.exists("data/metrics.csv"):
        os.remove("data/metrics.csv")

    user_count_range = range(18, 21)
    for users in user_count_range:
        run_locust_test(users)

    for users in user_count_range:
        theoretical_art, theoretical_util = tg.compute_theoretical_metrics(users, 1, 10, 20)
        theoretical_arts.append(theoretical_art)
        theoretical_utils.append(theoretical_util)
        print(f"[DEBUG] Computed theoretical util {theoretical_util} for {users} clients.")

    with open("data/metrics.csv", 'r', newline='') as response_time_csv:
        csv_reader = csv.reader(response_time_csv)
        for metrics in csv_reader:
            avg_response_times.append(float(metrics[0]))
            ci_lower.append(float(metrics[1]))
            ci_upper.append(float(metrics[2]))

    print(f"[DEBUG] Avg response times: {avg_response_times}")
    print(f"[DEBUG] CI lower: {ci_lower}")
    print(f"[DEBUG] CI upper: {ci_upper}")
    #tg.save_metrics_plot(user_count_range, theoretical_arts, theoretical_utils, avg_response_times,  "locust")


if __name__ == "__main__":
    main()
