import csv
import numpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from .load_generator import LoadGenerator


MIN_CLIENT_COUNT = 2


def get_average_response_times(max_client_count: int, arrival_rate: float, service_rate: float, client_request_time: int) -> tuple[list[float], list[float]]:

    theoretical_arts = []
    measured_arts = []

    for client_count in range(MIN_CLIENT_COUNT, max_client_count+1):
        theoretical_arts.append(compute_art(client_count, arrival_rate, service_rate, compute_forward_equations(
            rate_matrix(client_count, arrival_rate, service_rate), 0, client_request_time)))
        print(f"[DEBUG] Added theoretical ART number {client_count}.")

        lg = LoadGenerator(client_count, arrival_rate, "http://127.0.0.1:5000",
                           client_request_time, "./data")
        measured_arts.append(compute_average_response_time(lg))
        print(f"[DEBUG] Added measured ART number {client_count}.")

    return theoretical_arts, measured_arts


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
    total_response_time, number_of_responses = compute_total_response_time(
        load_generator.csv_filename)
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


def rate_matrix(client_count: int, arrival_rate: float, service_rate: float) -> numpy.ndarray:

    N = client_count
    Q = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        if i < N:  # Only if we are not at the maximum state
            Q[i, i + 1] = arrival_rate * (N-i)

        if i > 0:  # Only if we are not at the minimum state (0 clients)
            Q[i, i - 1] = service_rate

        if i == 0:  # Special case: state 0, where only arrivals are possible
            Q[i, i] = -arrival_rate * (N-i)
        elif i == N:  # Special case: state N, where only departures are possible
            Q[i, i] = -service_rate
        else:
            Q[i, i] = -(Q[i, i + 1] + Q[i, i - 1])

    return Q


def forward_equations(Q: numpy.ndarray, t_max: int, initial_state_probs: numpy.ndarray) -> numpy.ndarray:
    """
    Solve the forward Kolmogorov equations (dπ/dt = Q * π) numerically.

    Parameters:
    Q (numpy.ndarray): The rate (generator) matrix of the CTMC.
    t_max (int): The total time for the simulation.
    initial_state_probs (numpy.ndarray): Initial state probability distribution.

    Returns:
    solution (numpy.ndarray): Matrix of probabilities for each state at each time point.
    """

    t_points = np.linspace(0, t_max, 100)

    def ode_system(t, pi):
        return Q.T @ pi

    # Solve the system of ODEs using an initial condition
    solution = solve_ivp(ode_system, [0, t_max], initial_state_probs, t_eval=t_points)

    return solution.y.T


def compute_forward_equations(Q: numpy.ndarray, initial_state: int, t_max: int) -> numpy.ndarray:
    initial_state_probs = np.zeros(Q.shape[0])
    initial_state_probs[initial_state] = 1.0  # Start with 100% probability in the initial state
    probabilities_forward = forward_equations(Q, t_max, initial_state_probs)
    return probabilities_forward


def compute_art(N: int, arrival_rate: float, service_rate: float, probabilities_forward: numpy.ndarray) -> float:
    # changed because pi_N is the state where I have N clients waiting to be served
    rtt = N/(service_rate*(1-probabilities_forward[-1, 0]))
    art = rtt - 1/arrival_rate
    return art


def plot_art(N: int, theoretical_arts: list[float], measured_arts: list[float]) -> None:

    bar_width = 0.35
    x = np.arange(MIN_CLIENT_COUNT, N+1)

    plt.figure(figsize=(10, 6))
    plt.bar(x - bar_width / 2, theoretical_arts, bar_width,
            label='Theoretical', color='skyblue', edgecolor='black', alpha=1)
    plt.bar(x + bar_width / 2, measured_arts, bar_width,
            label='Measured', color='orange', edgecolor='black', alpha=1)
    plt.title("Average response time: theoretical vs measured")
    plt.xlabel("Number of clients")
    plt.ylabel("Average response time")
    plt.legend()
    # plt.show()
    plt.savefig("./data/art.png")
    plt.close()
