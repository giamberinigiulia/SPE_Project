import csv
import numpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from generator.load_generator import LoadGenerator



def get_average_response_times(client_counts: range, arrival_rate: float, service_rate: float, client_request_time: int) -> tuple[list[float], list[float], list[float]]:
    """
    Computes theoretical and measured average response times (ARTs) for a range of client counts.

    Parameters:
        max_client_count (int): The maximum number of clients to simulate.
        arrival_rate (float): The rate (in requests per second) at which clients generate requests.
        service_rate (float): The rate (in requests per second) at which the server processes requests.
        client_request_time (int): The time (in seconds) in which the client can send requests.

    Returns:
        tuple[list[float], list[float]]: 
            - A list of theoretical average response times.
            - A list of measured average response times.
    """

    theoretical_arts = []
    theoretical_utils = []
    measured_arts = []

    for client_count in client_counts:
        theoretical_art, theoretical_util = compute_theoretical_metrics(client_count, arrival_rate,
                                service_rate, client_request_time)
        theoretical_arts.append(theoretical_art)
        theoretical_utils.append(theoretical_util)
        
        print(f"[DEBUG] Computed theoretical ART for {client_count} clients.")

        measured_arts.append(compute_average_response_time(LoadGenerator(
            client_count, arrival_rate, "http://127.0.0.1:5000", client_request_time, "./data")))
        print(f"[DEBUG] Computed measured ART for {client_count} clients.")

    return theoretical_arts, measured_arts, theoretical_utils


def compute_average_response_time(load_generator: LoadGenerator) -> float:
    total_response_time = 0.0
    number_of_responses = 0
    
    load_generator.generate_load()

    with open(load_generator.csv_filename, 'r', newline='') as response_time_csv:
        response_time_reader = csv.reader(response_time_csv, delimiter=',')

        for response_times in response_time_reader:
            for time in response_times:
                total_response_time += float(time)
                number_of_responses += 1

    return total_response_time / number_of_responses


def generate_rate_matrix(client_count: int, arrival_rate: float, service_rate: float) -> numpy.ndarray:
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
    t_points = np.linspace(0, t_max, 100)

    def ode_system(t, pi):
        return Q.T @ pi

    # Solve the system of ODEs using an initial condition
    solution = solve_ivp(ode_system, [0, t_max], initial_state_probs, t_eval=t_points)

    return solution.y.T


def compute_forward_equations(rate_matrix: numpy.ndarray, initial_state: int, t_max: int) -> numpy.ndarray:
    initial_state_probs = np.zeros(rate_matrix.shape[0])
    initial_state_probs[initial_state] = 1.0  # Start with 100% probability in the initial state
    probabilities_forward = forward_equations(rate_matrix, t_max, initial_state_probs)
    return probabilities_forward


def compute_theoretical_metrics(client_count: int, arrival_rate: float, service_rate: float, client_request_time: int) -> tuple[float, float]:

    rate_matrix = generate_rate_matrix(client_count, arrival_rate, service_rate)
    state_probabilities = compute_forward_equations(
        rate_matrix=rate_matrix, initial_state=0, t_max=client_request_time)
    # pi_N is the state where I have all the clients waiting to be served
    utilization = 1 - state_probabilities[-1, 0]
    
    round_trip_time = client_count/(service_rate*(utilization))
    average_response_time = round_trip_time - 1/arrival_rate
    return average_response_time, utilization


def save_metrics_plot(client_counts: range, theoretical_arts: list[float], measured_arts: list[float], theoretical_utils: list[float], figure_name: str) -> None:
  
    bar_width = 0.35
    x = np.arange(client_counts.start, client_counts.stop)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.bar(x - bar_width / 2, theoretical_arts, bar_width,
            label='Theoretical ARTs', color='skyblue', edgecolor='black', alpha=1)
    ax1.bar(x + bar_width / 2, measured_arts, bar_width,
            label='Measured ARTs', color='orange', edgecolor='black', alpha=1)
    ax1.set_xlabel("Number of clients")
    ax1.set_ylabel("Average response time")
    ax1.set_title("Average response time and utilization: theoretical vs measured")
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.plot(x, theoretical_utils, label='Theoretical Utils', color='green', marker='o')
    ax2.set_ylabel("Utilization")
    ax2.legend(loc='upper right')

    fig.tight_layout()

    plt.savefig(f"./data/{figure_name}.png")
