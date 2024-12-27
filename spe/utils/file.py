from csv import writer
import os

CSV_FILENAME = "data/metrics.csv"

def delete_file_if_exists(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def write_csv(avg_response_time: float, lower_bound: float, upper_bound: float) -> None:
    with open(CSV_FILENAME, 'a', newline='') as csv_file:
        wr = writer(csv_file)
        wr.writerow([avg_response_time, lower_bound, upper_bound])
