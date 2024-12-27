from csv import writer, reader
import os
from typing import List, Tuple

from spe.utils.metrics import Metrics

CSV_FILENAME = "data/metrics.csv"


def delete_file_if_exists(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def write_csv(csv_filename: str, avg_response_time: float, lower_bound: float, upper_bound: float) -> None:
    with open(csv_filename, 'a', newline='') as csv_file:
        wr = writer(csv_file)
        wr.writerow([avg_response_time, lower_bound, upper_bound])


def read_csv(csv_filename: str) -> Metrics:
    avg_response_times = []
    ci_lower = []
    ci_upper = []

    with open(csv_filename, 'r', newline='') as csv_file:
        csv_reader = reader(csv_file)
        for metrics in csv_reader:
            avg_response_times.append(float(metrics[0]))
            ci_lower.append(float(metrics[1]))
            ci_upper.append(float(metrics[2]))
    
    return Metrics(avg_response_times, ci_lower, ci_upper)