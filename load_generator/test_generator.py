import matplotlib.pyplot as plt
import numpy as np
import csv

from generator import LoadGenerator


MAX_NUMBER_OF_CLIENTS = 5


def test_client_independence(enter_rate: float, exit_rate: float) -> None:
    '''Test the independence of clients.

    It tests that the response time of each client is around 1/enter_rate + 1/exit_rate.  

    Parameters:
    ----------
    enter_rate: float
        the rate at which the client enters in the system
    exit_rate: float
        the rate at which the client is served by the system
    '''

    expected_average_response_time = 1/enter_rate + 1/exit_rate
    average_response_times = get_average_response_times(enter_rate=enter_rate, max_time=10)
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
    '''Get the response times of independent load generators.

    Having the enter rate and the max time for making the requests, it returns the average response times for a set of
    load generators usings different number of clients.

    Parameters:
    ----------
    enter_rate: float
        the rate at which the client enters in the system
    max_time: int


    '''

    average_response_times = []

    # TODO: We want to skip the case with 0 client because it makes no sense, maybe we can capture this corner case by an exception
    for client_number in range(1, MAX_NUMBER_OF_CLIENTS+1):
        lg = LoadGenerator(number_clients=client_number, enter_rate=enter_rate,
                           max_time=max_time, target_url="https://example.com/")
        average_response_times.append(compute_average_response_time(lg))

    return average_response_times


def compute_average_response_time(load_generator: LoadGenerator) -> float:
    ''' Compute the average response time of the load generator.

    It returns the calculated average of registered times after generating the load on the server.

    Parameters:
    -----------
    load_generator: LoadGenerator
        the load generator object from which we want to extract the average

    Returns:
    --------
    The average of response times of the clients.
    '''

    load_generator.generate_load()
    total_response_time, number_of_responses = compute_total_response_time(load_generator.csv_filename)
    return total_response_time/number_of_responses


def compute_total_response_time(csv_filename: str) -> tuple[float, int]:
    '''Computes the total response time and the number of responses from a CSV file.

    This function reads a CSV file where each row contains response times recorded for a given client in seconds. 
    It calculates the total sum of all response times across all rows.

    Parameters:
    -----------
    csv_filename : str
        The path to the CSV file containing response times. Each row represents a set of response times
        separated by commas.

    Returns:
    --------
    tuple[float, int]
        A tuple where:
        - The first element (float) is the total sum of all response times.
        - The second element (int) is the number of responses.
    '''

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
