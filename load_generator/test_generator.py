import matplotlib.pyplot as plt
import numpy as np
import csv

from generator import LoadGenerator

NUMBER_OF_TRIALS = 5


def test_response_time(enter_rate: float, exit_rate: float) -> None:
    '''Test clients' requests independence

    '''

    expected_response_time = 1/enter_rate + 1/exit_rate   
    average_response_times = generate_mean_response_times(enter_rate=enter_rate, max_time=3)
    plot_response_times(expected_response_time, average_response_times)
    

def plot_response_times(expected_response_time: float, average_response_times: list[float]) -> None:
    plt.bar(x=range(1, len(average_response_times) +1), height=average_response_times)
    plt.axhline(y=expected_response_time, color='r', linestyle='--', label='1/lambda + 1/mu')
    plt.xlabel('Number of clients')
    plt.ylabel('Average response time')
    plt.title('Average response time by different numbers of clients')
    plt.legend()
    plt.show()

def generate_mean_response_times(enter_rate: float, max_time: int) -> list[float]:
    '''Computes the mean of the response times

    it returns a list containing the mean of reponse times computed using different numbers of clients
    '''
    mean_response_times = []

    # We want to skip the case with 0 client because it makes no sense, maybe we can capture this corner case
    for trial in range(1, NUMBER_OF_TRIALS):
        lg = LoadGenerator(clients_number=trial, enter_rate=enter_rate,
                           max_time=max_time, target_url="https://example.com/")
        mean_response_times.append(compute_mean_response_time(lg))

    return mean_response_times


def compute_mean_response_time(lg: LoadGenerator) -> float:
    # extract response times from the csv and compute the mean
    lg.generate_load()
    response_time, number_of_responses = fetch_times_from_csv(lg.csv_file_name)
    return response_time/number_of_responses


def fetch_times_from_csv(csv_filename: str) -> tuple[float, int]:
    response_time = 0.0
    number_of_responses = 0

    with open(csv_filename, 'r', newline='') as response_time_csv:
        response_time_reader = csv.reader(response_time_csv, delimiter=',')

        for row in response_time_reader:
            for value in row:
                response_time += float(value)
                number_of_responses += 1

    return response_time, number_of_responses


test_response_time(enter_rate=0.2, exit_rate=2)
