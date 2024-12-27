import os
import csv

import spe.generator.test_generator as tg
import spe.generator.load_generator as lg

TARGET_URL = "http://127.0.0.1:5000"

def run_load_generator(users: int, arrival_rate: float, target_url: str, client_request_time: int) -> None:
    load_generator = lg.LoadGenerator(users, arrival_rate, target_url, client_request_time)
    load_generator.generate_load()

def start_load_generator(user_range: range, arrival_rate: float, service_rate: float, client_request_time: int, server_count: int) -> None:
    print("[DEBUG] start_load_generator called")

    if os.path.exists("data/metrics.csv"):
        os.remove("data/metrics.csv")

    theoretical_arts = []
    theoretical_utils = []
    avg_response_times = []
    ci_lower = []
    ci_upper = []

    for users in user_range:
        run_load_generator(users, arrival_rate, TARGET_URL, client_request_time)
        theoretical_art, theoretical_util = tg.compute_theoretical_metrics(users, arrival_rate, service_rate, client_request_time, server_count)
        theoretical_arts.append(theoretical_art)
        theoretical_utils.append(theoretical_util)

    with open("data/metrics.csv", 'r', newline='') as response_time_csv:
        csv_reader = csv.reader(response_time_csv)
        for metrics in csv_reader:
            avg_response_times.append(float(metrics[0]))
            ci_lower.append(float(metrics[1]))
            ci_upper.append(float(metrics[2]))
    
    print("[DEBUG] ending simulation")
    os.remove("data/metrics.csv")
    tg.save_metrics_plot(user_range, theoretical_arts, theoretical_utils,
                         avg_response_times, ci_lower, ci_upper, f"simulation_s{service_rate}_a{arrival_rate}_t{client_request_time}_k{server_count}")

