from csv import writer, reader
import os
from typing import List, Tuple

from spe.utils.metric import MeasuredMetric

CSV_FILENAME = "data/metrics.csv"


def delete_file_if_exists(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def write_csv(csv_filename: str, avg_response_time: float, lower_bound: float, upper_bound: float) -> None:
    with open(csv_filename, 'a', newline='') as csv_file:
        wr = writer(csv_file)
        wr.writerow([avg_response_time, lower_bound, upper_bound])


def read_csv(csv_filename: str) -> List[MeasuredMetric]:
    measured_metrics = []

    with open(csv_filename, 'r', newline='') as csv_file:
        csv_reader = reader(csv_file)
        for metrics in csv_reader:
            avg_response_time = float(metrics[0])
            lower_bound = float(metrics[1])
            upper_bound = float(metrics[2])
            measured_metrics.append(MeasuredMetric(avg_response_time, lower_bound, upper_bound))
    
    return measured_metrics