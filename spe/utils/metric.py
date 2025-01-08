from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from scipy import stats
from scipy.integrate import solve_ivp

from spe.argument_parser import Config

INITIAL_STATE = 0

@dataclass
class Metric:
    avg_response_time: float

@dataclass
class MeasuredMetric(Metric):
    lower_bound: float
    upper_bound: float

@dataclass
class TheoreticalMetric(Metric):
    utilization: float

def compute_confidence_interval(data: List) -> Tuple[float, float]:
    mean = np.mean(data)
    std = np.std(data)
    number_of_observations = len(data)
    margin_of_error = (std / np.sqrt(number_of_observations)) * stats.t.ppf((1 + 0.90) / 2, number_of_observations - 1)
    return (mean - margin_of_error, mean + margin_of_error)


def compute_mean(data: List) -> float:
    return sum(data)/len(data)


def compute_theoretical_metrics(system_config: Config) -> List[TheoreticalMetric]:
    theoretical_metrics = []
    service_rate = system_config.service_rate
    arrival_rate = system_config.arrival_rate
    user_range = system_config.user_range
    user_request_time = system_config.user_request_time
    number_of_servers = system_config.number_of_servers

    for number_of_users in user_range:
        rate_matrix = _generate_rate_matrix(number_of_users, arrival_rate, service_rate, number_of_servers)
        state_probabilities = _compute_forward_equations(rate_matrix, INITIAL_STATE, user_request_time)

        # pi_N is the state where I have all the clients waiting to be served
        if number_of_servers == 1:
            utilization = 1 - state_probabilities[-1, 0]
            round_trip_time = number_of_users/(service_rate*(utilization))
            average_response_time = round_trip_time - 1/arrival_rate
        else:
            utilization = 0
            mean_queue_length = 0
            for i, prob in enumerate(state_probabilities[-1]):
                utilization += min(i, number_of_servers) * prob
                mean_queue_length += i * prob
            utilization = utilization / number_of_servers    # normalized between 0 and number_of_servers
            average_response_time = mean_queue_length / (arrival_rate * (1 - state_probabilities[-1, number_of_users]))\
            
        theoretical_metrics.append(TheoreticalMetric(average_response_time, utilization))

    return theoretical_metrics


def _generate_rate_matrix(number_of_users: int, arrival_rate: float, service_rate: float, number_of_servers: int) -> np.ndarray:
    N = number_of_users
    k = number_of_servers
    Q = np.zeros((N + 1, N + 1))

    # The service rate depends on the number of clients and the number of servers
    for i in range(N + 1):
        if i < N:
            Q[i, i + 1] = arrival_rate * (N - i)

        if i > 0:
            Q[i, i - 1] = service_rate * min(i, k)

        if i == 0:  # Only arrivals are possible
            Q[i, i] = -arrival_rate * (N - i)
        elif i == N:  # Only departures are possible
            Q[i, i] = -service_rate * min(i, k)
        else:
            Q[i, i] = -(Q[i, i + 1] + Q[i, i - 1])

    return Q


def _forward_equations(Q: np.ndarray, t_max: int, initial_state_probs: np.ndarray) -> np.ndarray:
    t_points = np.linspace(0, t_max, 100)

    def ode_system(t, pi):
        return Q.T @ pi

    # Solve the system of ODEs using an initial condition
    solution = solve_ivp(ode_system, [0, t_max], initial_state_probs, t_eval=t_points)

    return solution.y.T


def _compute_forward_equations(rate_matrix: np.ndarray, initial_state: int, t_max: int) -> np.ndarray:
    initial_state_probs = np.zeros(rate_matrix.shape[0])
    initial_state_probs[initial_state] = 1.0
    probabilities_forward = _forward_equations(rate_matrix, t_max, initial_state_probs)
    return probabilities_forward
