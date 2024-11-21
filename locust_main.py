import os
import subprocess
import csv

import generator.test_generator as tg


def run_locust_test(users):
    # Command to run Locust in headless mode
    command = [
        "locust", "--headless",
        "-u", str(users),
        "-r", str(users),  # Spawn rate matches the user count
        "-t", "20s",  # Test duration of 20 seconds
        "-H", "http://127.0.0.1:5000"
    ]

    subprocess.run(command, capture_output=True, text=True)  # maybe remove capture and text


def main():
    if os.path.exists("data/avg_response_time.csv"):
        os.remove("data/avg_response_time.csv")

    user_counts = range(2, 11)

    for users in user_counts:
        run_locust_test(users)

    avg_response_times = []
    with open("data/avg_response_time.csv", 'r', newline='') as response_time_csv:
        rows = csv.reader(response_time_csv)
        for row in rows:
            avg_response_times.append(float(row[0]))

    theoretical_arts = []

    for users in user_counts:
        theoretical_arts.append(tg.compute_art(
            client_count=users, arrival_rate=1, service_rate=10, client_request_time=20))
    
    tg.plot_art(10, theoretical_arts, avg_response_times, "locust")


if __name__ == "__main__":
    main()