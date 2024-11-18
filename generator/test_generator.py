import csv
import numpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from .load_generator import LoadGenerator


MIN_CLIENT_COUNT = 2


def get_average_response_times(max_client_count: int, arrival_rate: float, service_rate: float, client_request_time: int) -> tuple[list[float], list[float]]:
    '''
    TODO: add documentation
    '''
    theoretical_arts = []
    measured_arts = []

    for client_count in range(MIN_CLIENT_COUNT, max_client_count+1):
        theoretical_arts.append(compute_art(client_count, arrival_rate,
                                service_rate, client_request_time))
        print(f"[DEBUG] Computed theoretical ART for {client_count} clients.")

        measured_arts.append(compute_average_response_time(LoadGenerator(
            client_count, arrival_rate, "http://127.0.0.1:5000", client_request_time, "./data")))
        print(f"[DEBUG] Computed measured ART for {client_count} clients.")

    return theoretical_arts, measured_arts


def compute_average_response_time(load_generator: LoadGenerator) -> float:
    load_generator.generate_load()
    total_response_time, number_of_responses = compute_total_response_time(
        load_generator.csv_filename)
    return total_response_time/number_of_responses


def compute_total_response_time(csv_filename: str) -> tuple[float, int]:
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


def compute_art(client_count: int, arrival_rate: float, service_rate: float, client_request_time: int) -> float:
    '''
    TODO: add documentation because we're exposing it
    '''

    Q = rate_matrix(client_count, arrival_rate, service_rate)
    probabilities_forward = compute_forward_equations(
        Q=Q, initial_state=0, t_max=client_request_time)
    # pi_N is the state where I have all the clients waiting to be served
    rtt = client_count/(service_rate*(1-probabilities_forward[-1, 0]))
    art = rtt - 1/arrival_rate
    return art


def plot_art(client_count: int, theoretical_arts: list[float], measured_arts: list[float]) -> None:
    '''
    TODO: add documentation
    '''
    
    bar_width = 0.35
    x = np.arange(MIN_CLIENT_COUNT, client_count + 1)

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
