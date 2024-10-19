'''Testing properties of load generator.
'''

import matplotlib.pyplot as plt
import numpy as np
import csv

from generator import LoadGenerator

# Using high values will cause the test to run for a long time. 
# It takes around 2 minutes in my machine.
MAX_NUMBER_OF_CLIENTS = 3


def test_client_independence(enter_rate: float, exit_rate: float) -> None:
    '''TODO: after Lorenzo's check

    '''

    expected_average_response_time = 1/enter_rate + 1/exit_rate
    average_response_times = get_average_response_times(enter_rate=enter_rate, max_time=20)
    plot_average_response_times(expected_average_response_time, average_response_times)


def plot_average_response_times(expected_average_response_time: float, average_response_times: list[float]) -> None:
    plt.bar(x=range(1, len(average_response_times) + 1), height=average_response_times)
    plt.axhline(y=expected_average_response_time, color='r', linestyle='--', label='1/lambda + 1/mu')
    plt.xlabel('Number of clients')
    plt.ylabel('Average response time')
    plt.title('Average response time by different numbers of clients')
    plt.legend()
    plt.show()


def get_average_response_times(enter_rate: float, max_time: int) -> list[float]:
    '''
    Having the enter rate and the max time for making the requests, it returns the average response times for a set of
    load generators usings different number of clients.
    '''
    average_response_times = []

    # We want to skip the case with 0 client because it makes no sense, maybe we can capture this corner case by an exception
    for client_number in range(1, MAX_NUMBER_OF_CLIENTS+1):
        lg = LoadGenerator(clients_number=client_number, enter_rate=enter_rate,
                           max_time=max_time, target_url="https://example.com/")
        average_response_times.append(compute_mean_response_time(lg))

    return average_response_times


def compute_mean_response_time(load_generator: LoadGenerator) -> float:
    ''' Extract response times from csv and return the computed average.
    '''
    load_generator.generate_load()
    total_response_time, number_of_responses = get_total_response_time(load_generator.csv_file_name)
    return total_response_time/number_of_responses


def get_total_response_time(csv_filename: str) -> tuple[float, int]:
    # we can pass the load generator instead of the csv filename, maybe it's a better approach for hiding implementation details
    total_response_time = 0.0
    number_of_responses = 0

    with open(csv_filename, 'r', newline='') as response_time_csv:
        system_response_times = csv.reader(response_time_csv, delimiter=',')

        for client_response_times in system_response_times:
            for response_time in client_response_times:
                total_response_time += float(response_time)
                number_of_responses += 1

    return total_response_time, number_of_responses


if __name__ == '__main__':
    test_client_independence(enter_rate=4, exit_rate=8)
