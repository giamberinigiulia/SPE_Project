"""This module provides tools for computing theoretical average response time (ART), utilization and statistics
related to system performance. 
"""

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from scipy import stats
from scipy.integrate import solve_ivp

from spe.argument_parser import Config

INITIAL_STATE = 0
CONFIDENCE_LEVEL = 0.90


@dataclass
class MeasuredMetric():
    avg_response_time: float
    lower_bound: float
    upper_bound: float


@dataclass
class TheoreticalMetric():
    avg_response_time: float
    utilization: float


def compute_mean(data: List[float]) -> float:
    return sum(data) / len(data)


def compute_confidence_intervals(data: List[float]) -> Tuple[float, float]:
    """    
    Computes the lower and upper bounds of a confidence interval using
    the t-distribution.

    Args:
        data: List of numerical observations (measurements).

    Returns:
        A tuple containing (lower_bound, upper_bound) of the confidence interval.
    """
    mean = np.mean(data)
    std = np.std(data)
    number_of_observations = len(data)
    margin_of_error = (std / np.sqrt(number_of_observations)) * \
        stats.t.ppf((1 + CONFIDENCE_LEVEL) / 2, number_of_observations - 1)
    return (mean - margin_of_error, mean + margin_of_error)


def compute_theoretical_metrics(system_config: Config) -> List[TheoreticalMetric]:
    """
    Computes the average reponse time and the server utilization for a closed M/M/c queue system.

    Args:
        system_config: Configuration containing service parameters and user range.

    Returns:
        A list of TheoreticalMetric objects, one for each client count in the user_range.
    """
    arrival_rate = system_config.arrival_rate
    service_rate = system_config.service_rate
    c = system_config.number_of_servers
    metrics = []

    for num_clients in system_config.user_range:
        Q = _build_rate_matrix(num_clients, arrival_rate, service_rate, c)
        probabilities_over_time = _compute_forward_equations(Q, t_max=200)
        steady_state = probabilities_over_time[-1]
        theoretical = _calculate_metrics_from_steady_state(
            steady_state, num_clients, c, service_rate
        )
        metrics.append(theoretical)

    return metrics


def _build_rate_matrix(N: int, arrival_rate: float, service_rate: float, c: int) -> np.ndarray:
    Q = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        # Arrivals (thinking clients generate requests)
        if i < N:
            Q[i, i + 1] = (N - i) * arrival_rate
        # Departures (servers complete requests)
        if i > 0:
            Q[i, i - 1] = min(i, c) * service_rate
        Q[i, i] = -sum(Q[i, :])

    return Q


def _calculate_metrics_from_steady_state(
    steady_state: np.ndarray,
    num_clients: int,
    c: int,
    service_rate: float
) -> TheoreticalMetric:
    """Calculate key performance metrics from the steady state distribution."""
    L = sum(i * steady_state[i] for i in range(num_clients + 1))
    X = sum(min(i, c) * service_rate * steady_state[i] for i in range(1, num_clients + 1))
    average_response_time = L / X if X > 0 else float('inf')
    busy_servers = sum(min(i, c) * steady_state[i] for i in range(1, num_clients + 1))
    utilization = busy_servers / c

    return TheoreticalMetric(average_response_time, utilization)


def _compute_forward_equations(Q: np.ndarray, t_max: int) -> np.ndarray:
    initial_state_probs = np.zeros(Q.shape[0])
    initial_state_probs[INITIAL_STATE] = 1.0
    probabilities_forward = _forward_equations(Q, t_max, initial_state_probs)
    return probabilities_forward


def _forward_equations(Q: np.ndarray, t_max: int, initial_state_probs: np.ndarray) -> np.ndarray:
    t_points = np.linspace(0, t_max, 100)

    def ode_system(t, pi):
        return Q.T @ pi

    solution = solve_ivp(ode_system, [0, t_max], initial_state_probs, t_eval=t_points)
    return solution.y.T
