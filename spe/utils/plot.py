"""This module provides function to generate and save plots for visualizing 
theoretical and measured metrics from queue simulation experiments.
"""
import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from spe.utils.argument_parser import Config
from spe.utils.metric import MeasuredMetric, TheoreticalMetric

FIGURE_FOLDER = "data/"


def save_metrics_plot(system_config: Config, theoretical_metrics: List[TheoreticalMetric], measured_metrics: List[MeasuredMetric]) -> None:
    """
    Creates and saves visualization comparing theoretical and measured performance metrics.

    This function generates a plot with two y-axes:
    1. Left y-axis: Bar chart comparing theoretical vs measured average response times (ARTs)
       with confidence intervals for measured values
    2. Right y-axis: Line plot comparing theoretical vs measured server utilization

    The plot is saved as a PNG file in the data directory with a filename derived from
    the system configuration parameters.

    Args:
        system_config: Configuration object containing simulation parameters
        theoretical_metrics: List of theoretical performance metrics for different client counts
        measured_metrics: List of measured performance metrics for different client counts

    Note:
        The function automatically creates the data directory if it doesn't exist.
        The x-axis always represents the number of clients in the simulation.
    """
    os.makedirs(FIGURE_FOLDER, exist_ok=True)

    user_range = system_config.user_range
    theoretical_arts = [metric.avg_response_time for metric in theoretical_metrics]
    theoretical_utils = [metric.utilization for metric in theoretical_metrics]
    avg_response_times = [metric.avg_response_time for metric in measured_metrics]
    lower_bounds = [metric.lower_bound for metric in measured_metrics]
    upper_bounds = [metric.upper_bound for metric in measured_metrics]
    measured_utils = [metric.utilization for metric in measured_metrics]
    x = np.arange(user_range.start, user_range.stop)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel("Number of clients")
    ax1.set_ylabel("Average response time")
    plt.suptitle('Average response time and utilization: theoretical vs measured', fontsize=14)
    simulation_info = (
        f"[$\\mu$] = {system_config.service_rate}, "
        f"[$\\lambda$] = {system_config.arrival_rate}, "
        f"[$t$] = {system_config.user_request_time}, "
        f"[$k$] = {system_config.number_of_servers}"
    )
    plt.title(simulation_info, fontsize=10, loc='center')

    bar_width = 0.35
    ax1.bar(x - bar_width / 2, theoretical_arts, bar_width,
            label='Theoretical ARTs', color='skyblue', edgecolor='black', alpha=1)
    ax1.bar(x + bar_width / 2, avg_response_times, bar_width,
            label='Measured ARTs', color='orange', edgecolor='black', alpha=1)
    error = [avg_response_times[i] - lower_bounds[i] for i in range(len(avg_response_times))]
    ax1.errorbar(x + bar_width / 2, avg_response_times, yerr=[error, [upper_bounds[i] - avg_response_times[i] for i in range(
        len(avg_response_times))]], fmt='none', ecolor='black', capsize=5, label='Confidence Interval')
    ax1.legend(loc='upper left', bbox_to_anchor=(0, 1))

    ax2 = ax1.twinx()
    ax2.plot(x, theoretical_utils, label='Theoretical Utils', color='green', marker='o')
    ax2.plot(x, measured_utils, label='Measured Utils', color='purple', marker='^')
    ax2.set_ylabel("Utilization")
    ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.85))

    fig.tight_layout()
    figure_name = f"simulation_s{system_config.service_rate}_a{system_config.arrival_rate}_t{system_config.user_request_time}_k{system_config.number_of_servers}"
    figure_path = os.path.join(FIGURE_FOLDER, f"{figure_name}.png")
    plt.savefig(figure_path)
    plt.close()
