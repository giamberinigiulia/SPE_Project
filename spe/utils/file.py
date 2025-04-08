"""This module provides utility functions for handling CSV files and managing file operations."""
from csv import writer, reader
import os
from typing import List

from spe.utils.metric import MeasuredMetric

CSV_PATH = "data/metrics.csv"


def write_metrics_to_csv(path: str, metrics: MeasuredMetric) -> None:
    with open(path, 'a', newline='') as csv_file:
        wr = writer(csv_file)
        wr.writerow([metrics.avg_response_time, metrics.lower_bound,
                    metrics.upper_bound, metrics.utilization])


def read_metrics_from_csv(path: str) -> List[MeasuredMetric]:
    measured_metrics = []

    with open(path, 'r', newline='') as csv_file:
        csv_reader = reader(csv_file)
        for metrics in csv_reader:
            avg_response_time = float(metrics[0])
            lower_bound = float(metrics[1])
            upper_bound = float(metrics[2])
            utilization = float(metrics[3])
            measured_metrics.append(MeasuredMetric(
                avg_response_time, lower_bound, upper_bound, utilization))

    return measured_metrics


def delete_file_if_exists(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


def truncate_file(path: str) -> None:
    """Clear the contents of a file without closing the handle."""
    try:
        with open(path, 'w') as f:
            f.truncate(0)
    except Exception as e:
        print(f"Error truncating file {path}: {e}")
