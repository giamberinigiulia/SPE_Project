import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.integrate import solve_ivp

from generator.load_generator import LoadGenerator


MAX_NUMBER_OF_CLIENTS = 5


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
    for client_number in range(2, MAX_NUMBER_OF_CLIENTS+1):
        lg = LoadGenerator(number_clients=client_number, enter_rate=enter_rate,
                           max_time=max_time, target_url="http://127.0.0.1:5000")
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


def rate_matrix(num_clients, arrival_rate, service_rate):

    N = num_clients
    R = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        if i < N:  # Only if we are not at the maximum state
            R[i, i + 1] = arrival_rate * (N-i)

        if i > 0:  # Only if we are not at the minimum state (0 clients)
            R[i, i - 1] = service_rate

        if i == 0:  # Special case: state 0, where only arrivals are possible
            R[i, i] = -arrival_rate * (N-i)
        elif i == N:  # Special case: state N, where only departures are possible
            R[i, i] = -service_rate
        else:
            R[i, i] = -(R[i, i + 1] + R[i, i - 1])

    return R


def forward_equations(Q, t_max, initial_state_probs):
    """
    Solve the forward Kolmogorov equations (dπ/dt = Q * π) numerically.

    Parameters:
    Q (numpy.ndarray): The rate (generator) matrix of the CTMC.
    t_max (float): The total time for the simulation.
    initial_state_probs (numpy.ndarray): Initial state probability distribution.

    Returns:
    probabilities (numpy.ndarray): Matrix of probabilities for each state at each time point.
    """

    t_points = np.linspace(0, t_max, 100)

    def ode_system(t, pi):
        return Q.T @ pi

    # Solve the system of ODEs using an initial condition
    solution = solve_ivp(ode_system, [0, t_max], initial_state_probs, t_eval=t_points)

    return solution.y.T


def compute_forward_equations(Q, initial_state, t_max):
    initial_state_probs = np.zeros(Q.shape[0])
    initial_state_probs[initial_state] = 1.0  # Start with 100% probability in the initial state
    probabilities_forward = forward_equations(Q, t_max, initial_state_probs)
    return probabilities_forward


if __name__ == '__main__':
    num_clients = 4
    arrival_rate = 2
    service_rate = 3
    R = rate_matrix(num_clients, arrival_rate, service_rate)
    print(compute_forward_equations(R, 0, 30))
