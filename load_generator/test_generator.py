import matplotlib.pyplot as plt
import numpy as np
import csv

from generator import LoadGenerator


def plot_response_time_test(enter_rate: float, exit_rate: float) -> None:
    '''Test clients' requests independence

    '''

    wanted_waiting_time = 1/enter_rate + 1/exit_rate
    got = np.random.randint(50, size=30)  # TODO: change with array of waiting time values

    plt.bar(x=range(1, 31), height=got)  # TODO: change x and height with correct values from generator function
    plt.axhline(y=wanted_waiting_time, color='r', linestyle='--', label='1/lambda + 1/mu')
    plt.xlabel('Number of clients')
    plt.ylabel('Waiting time')
    plt.title('Waiting times by different numbers of clients')
    plt.legend()

    plt.show()


def generate_mean_response_times(enter_rate: float, max_time: int, number_rounds: int) -> list[float]:
    '''Computes the mean of the response times

    it returns a list containing the mean of reponse times computed using different numbers of clients
    '''
    mean_response_times = []

    for n in range(number_rounds):
        lg = LoadGenerator(clients_number=n, enter_rate=enter_rate, max_time=max_time, target_url="https://example.com/")
        
    return

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


lg = LoadGenerator(clients_number=5, enter_rate=0.2, max_time=5, target_url="https://example.com/")
print(compute_mean_response_time(lg))
#plot_response_time_test(0.2, 2)
