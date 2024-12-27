from typing import List, Tuple

import numpy as np
from scipy import stats
from scipy.integrate import solve_ivp



def compute_confidence_interval(data: List) -> Tuple[float, float]:
    mean = np.mean(data)
    std = np.std(data)
    number_of_observations = len(data)
    margin_of_error = (std / np.sqrt(number_of_observations)) * stats.t.ppf((1 + 0.95) / 2, number_of_observations - 1)
    return (mean - margin_of_error, mean + margin_of_error)


def compute_mean(data: List) -> float:
    return sum(data)/len(data)

def generate_rate_matrix(client_count: int, arrival_rate: float, service_rate: float, server_count: int) -> np.ndarray:
    N = client_count
    k = server_count
    Q = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        if i < N:  # Only if we are not at the maximum state
            Q[i, i + 1] = arrival_rate * (N - i)

        if i > 0:  # Only if we are not at the minimum state (0 clients)
            # The service rate depends on the number of clients and the number of servers
            Q[i, i - 1] = service_rate * min(i, k)

        if i == 0:  # Special case: state 0, where only arrivals are possible
            Q[i, i] = -arrival_rate * (N - i)
        elif i == N:  # Special case: state N, where only departures are possible
            Q[i, i] = -service_rate * min(i, k)
        else:
            Q[i, i] = -(Q[i, i + 1] + Q[i, i - 1])

    return Q


def forward_equations(Q: np.ndarray, t_max: int, initial_state_probs: np.ndarray) -> np.ndarray:
    t_points = np.linspace(0, t_max, 100)

    def ode_system(t, pi):
        return Q.T @ pi

    # Solve the system of ODEs using an initial condition
    solution = solve_ivp(ode_system, [0, t_max], initial_state_probs, t_eval=t_points)

    return solution.y.T


def compute_forward_equations(rate_matrix: np.ndarray, initial_state: int, t_max: int) -> np.ndarray:
    initial_state_probs = np.zeros(rate_matrix.shape[0])
    initial_state_probs[initial_state] = 1.0  # Start with 100% probability in the initial state
    probabilities_forward = forward_equations(rate_matrix, t_max, initial_state_probs)
    return probabilities_forward


def compute_theoretical_metrics(client_count: int, arrival_rate: float, service_rate: float, client_request_time: int, server_count: int) -> Tuple[float, float]:

    rate_matrix = generate_rate_matrix(client_count, arrival_rate, service_rate, server_count)
    state_probabilities = compute_forward_equations(
        rate_matrix=rate_matrix, initial_state=0, t_max=client_request_time)

    if server_count == 1:
        # pi_N is the state where I have all the clients waiting to be served
        utilization = 1 - state_probabilities[-1, 0]
        round_trip_time = client_count/(service_rate*(utilization))
        average_response_time = round_trip_time - 1/arrival_rate
    else:
        utilization = 0
        mean_queue_length = 0
        for i, prob in enumerate(state_probabilities[-1]):
            utilization += min(i, server_count) * prob
            mean_queue_length += i * prob
        utilization = utilization / server_count    # normalized between 0 and server_count
        average_response_time = mean_queue_length / (arrival_rate * (1 - state_probabilities[-1, client_count]))
    return average_response_time, utilization
