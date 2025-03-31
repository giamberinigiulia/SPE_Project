"""
Metric Computation Utilities for SPE Project.

This module provides tools for computing both measured and theoretical metrics
related to system performance. It includes statistical functions, helper methods
for solving forward equations, and theoretical metrics for closed M/M/c queue systems.

Key Features:
1. Data Classes:
   - `Metric`: Base class for metrics.
   - `MeasuredMetric`: Includes confidence intervals for measured metrics.
   - `TheoreticalMetric`: Includes utilization for theoretical metrics.

2. Statistical Functions:
   - `compute_confidence_interval`: Calculates confidence intervals for a dataset.
   - `compute_mean`: Computes the mean of a dataset.

3. Forward Equations:
   - `_forward_equations`: Solves forward equations for a given rate matrix.
   - `_compute_forward_equations`: Computes probabilities over time for a Markov chain.

4. Theoretical Metrics:
   - `compute_theoretical_metric_closed`: Computes metrics for a closed M/M/c queue.
   - `compute_theoretical_metrics`: Computes metrics for a range of client counts.

Usage:
Import this module to compute metrics for system performance analysis.

Example:
    from spe.utils.metric import compute_theoretical_metrics
    metrics = compute_theoretical_metrics(system_config)
"""

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from scipy import stats
from scipy.integrate import solve_ivp

from spe.argument_parser import Config

INITIAL_STATE = 0

# --- Data Classes ---

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

# --- Statistical functions ---

def compute_confidence_interval(data: List[float]) -> Tuple[float, float]:
    mean = np.mean(data)
    std = np.std(data)
    number_of_observations = len(data)
    margin_of_error = (std / np.sqrt(number_of_observations)) * stats.t.ppf((1 + 0.90) / 2, number_of_observations - 1)
    return (mean - margin_of_error, mean + margin_of_error)

def compute_mean(data: List[float]) -> float:
    return sum(data) / len(data)

# --- Forward Equations helper functions ---

def _forward_equations(Q: np.ndarray, t_max: int, initial_state_probs: np.ndarray) -> np.ndarray:
    t_points = np.linspace(0, t_max, 100)

    def ode_system(t, pi):
        return Q.T @ pi

    solution = solve_ivp(ode_system, [0, t_max], initial_state_probs, t_eval=t_points)
    return solution.y.T

def _compute_forward_equations(Q: np.ndarray, initial_state: int, t_max: int) -> np.ndarray:
    initial_state_probs = np.zeros(Q.shape[0])
    initial_state_probs[initial_state] = 1.0
    probabilities_forward = _forward_equations(Q, t_max, initial_state_probs)
    return probabilities_forward


# --- Theoretical Metrics for a Closed M/M/c Queue with N Independent Clients ---
#
# In this closed system, there are N clients.
# Each client waits an exponential time (with rate λ) before making a new request,
# while the service is provided by c servers, each serving at rate µ.
#
# The state i represents the number of busy servers.
# For state 0 ≤ i < m (with m = min(c, N)):
#   - Arrival (i → i+1) rate is (N - i)*λ
#   - Departure (i → i-1) rate is i * µ (for i > 0)
# In state m, no new arrivals are allowed.
#
# Then:
#   L = Σ (i * π[i])         [average busy servers]
#   X = Σ (i * µ * π[i])       [throughput]
#   R = L / X                if X > 0 else ∞ (response time)
#   utilization = X / (c * µ)  (server utilization)
#

def compute_theoretical_metric_closed(system_config: Config, num_clients: int) -> TheoreticalMetric:
    arrival_rate = system_config.arrival_rate   # λ (per client)
    service_rate = system_config.service_rate   # µ
    c = system_config.number_of_servers         # number of servers
    
    # State space should represent number of clients in system (0 to N)
    # Not just the number of busy servers
    N = num_clients
    
    # Build rate matrix Q with dimension (N+1) x (N+1)
    Q = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        # Arrival: new request from a thinking client (only if there are idle clients)
        if i < N:
            Q[i, i + 1] = (N - i) * arrival_rate
        
        # Departure: servicing clients (limited by number of busy servers and available servers)
        if i > 0:
            # Effective service rate = min(i, c) * service_rate
            # (can't serve more clients than servers available)
            Q[i, i - 1] = min(i, c) * service_rate
            
        Q[i, i] = -sum(Q[i, :])
    
    t_max = 200  # integration time for convergence
    probabilities_over_time = _compute_forward_equations(Q, 0, t_max)
    steady_state = probabilities_over_time[-1]

    # Average number of clients in the system (both being served and waiting)
    L = sum(i * steady_state[i] for i in range(N + 1))
    
    # Throughput is the overall departure rate
    X = sum(min(i, c) * service_rate * steady_state[i] for i in range(1, N + 1))
    
    # Response time via Little's Law
    R = L / X if X > 0 else float('inf')
    
    # Utilization is average number of busy servers divided by total servers
    busy_servers = sum(min(i, c) * steady_state[i] for i in range(1, N + 1))
    utilization = busy_servers / c
    
    return TheoreticalMetric(avg_response_time=R, utilization=utilization)

def compute_theoretical_metrics(system_config: Config) -> List[Tuple[int, TheoreticalMetric]]:
    """
    Computes theoretical metrics for each client count in the system_config.user_range.
    
    Args:
        system_config: Configuration containing service parameters and user range.
        
    Returns:
        A list of tuples, each containing (number_of_clients, theoretical_metric).
    """
    metrics = []
    for num_clients in system_config.user_range:
        metric = compute_theoretical_metric_closed(system_config, num_clients)
        metrics.append( metric)
    return metrics

