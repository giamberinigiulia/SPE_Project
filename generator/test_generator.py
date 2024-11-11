import csv
import numpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from .load_generator import LoadGenerator


INIT_NUMBER_OF_CLIENTS = 2
MAX_NUMBER_OF_CLIENTS = 10


def get_average_response_times(arrival_rate: float, max_time: int) -> tuple[list[float], list[float]]:

    theoretical_arts = []
    measured_arts = []

    for num_clients in range(INIT_NUMBER_OF_CLIENTS, MAX_NUMBER_OF_CLIENTS+1):
        theoretical_arts.append(compute_art(N=num_clients, arrival_rate=arrival_rate, service_rate=20, probabilities_forward=compute_forward_equations(
            Q=rate_matrix(num_clients=num_clients, arrival_rate=arrival_rate, service_rate=20), initial_state=0, t_max=max_time)))
        print(f"[DEBUG] Added theoretical ART number {num_clients}.")

        lg = LoadGenerator(num_clients=num_clients, arrival_rate=arrival_rate,
                           max_time=max_time, csv_directory="./data", target_url="http://127.0.0.1:5000")
        measured_arts.append(compute_average_response_time(lg))
        print(f"[DEBUG] Added measured ART number {num_clients}.")

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


def rate_matrix(num_clients: int, arrival_rate: float, service_rate: float) -> numpy.ndarray:

    N = num_clients
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
    rtt = N/(service_rate*(1-probabilities_forward[-1, 0])) # changed because pi_N is the state where I have N clients waiting to be served
    art = rtt - 1/arrival_rate
    return art


def plot_art(N: int, theoretical_arts: list[float], measured_arts: list[float]) -> None:

    bar_width = 0.35
    x = np.arange(INIT_NUMBER_OF_CLIENTS, MAX_NUMBER_OF_CLIENTS+1)

    plt.figure(figsize=(10, 6))
    plt.bar(x - bar_width / 2, theoretical_arts, bar_width, label='Theoretical', color='skyblue', edgecolor='black', alpha=1)
    plt.bar(x + bar_width / 2, measured_arts, bar_width, label='Measured', color='orange', edgecolor='black', alpha=1)
    plt.title("Average response time: theoretical vs measured")
    plt.xlabel("Number of clients")
    plt.ylabel("Average response time")
    plt.legend()
    #plt.show()
    plt.savefig("./data/art.png")
    plt.close()


if __name__ == '__main__':
    # num_clients = 4
    # arrival_rate = 2
    # service_rate = 3
    # Q = rate_matrix(num_clients, arrival_rate, service_rate)
    # prob = compute_forward_equations(Q, 0, 30)
    # print(prob)
    #print(get_average_response_times(7, 5))

    #theoretical_arts, measured_arts = get_average_response_times(2, 20)
    #plot_art(MAX_NUMBER_OF_CLIENTS, theoretical_arts, measured_arts)
    Q = rate_matrix(5, 2, 8)
    prob = compute_forward_equations(Q, 0, 30)
    print(prob)