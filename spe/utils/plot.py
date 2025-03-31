"""
SPE Project Plotting Utilities.

This module provides functions to generate and save plots for visualizing 
theoretical and measured metrics, such as average response times and utilization.

Functions:
- `save_metrics_plot`: Creates a bar plot comparing theoretical and measured 
  average response times, along with a line plot for theoretical utilization.

Modules Used:
- `matplotlib.pyplot`: For creating and saving plots.
- `numpy`: For numerical operations.
- `spe.argument_parser.Config`: For accessing system configuration details.
- `spe.utils.metric`: For handling theoretical and measured metrics.

Constants:
- `FIGURE_FOLDER`: Directory where the generated plots are saved.

Usage:
Call the `save_metrics_plot` function with the required arguments to generate 
and save a plot.

Example:
    save_metrics_plot(system_config, theoretical_metrics, measured_metrics)
"""

from typing import List

import matplotlib.pyplot as plt
import numpy as np

from spe.argument_parser import Config
from spe.utils.metric import MeasuredMetric, TheoreticalMetric

FIGURE_FOLDER = "data/"

def save_metrics_plot(system_config: Config, theoretical_metrics: List[TheoreticalMetric], measured_metrics: List[MeasuredMetric]) -> None:
    user_range = system_config.user_range
    theoretical_arts = [metric.avg_response_time for metric in theoretical_metrics]
    theoretical_utils = [metric.utilization for metric in theoretical_metrics]
    avg_response_times = [metric.avg_response_time for metric in measured_metrics]
    lower_bounds = [metric.lower_bound for metric in measured_metrics]
    upper_bounds = [metric.upper_bound for metric in measured_metrics]

    bar_width = 0.35
    x = np.arange(user_range.start, user_range.stop)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.bar(x - bar_width / 2, theoretical_arts, bar_width,
            label='Theoretical ARTs', color='skyblue', edgecolor='black', alpha=1)
    ax1.bar(x + bar_width / 2, avg_response_times, bar_width,
            label='Measured ARTs', color='orange', edgecolor='black', alpha=1)

    # Calculate and add error bars for confidence intervals
    error = [avg_response_times[i] - lower_bounds[i] for i in range(len(avg_response_times))]
    ax1.errorbar(x + bar_width / 2, avg_response_times, yerr=[error, [upper_bounds[i] - avg_response_times[i] for i in range(
        len(avg_response_times))]], fmt='none', ecolor='black', capsize=5, label='Confidence Interval')

    ax1.set_xlabel("Number of clients")
    ax1.set_ylabel("Average response time")
    # ax1.set_title("Average response time and utilization: theoretical vs measured", loc='center')
    
    plt.suptitle('Average response time and utilization: theoretical vs measured', fontsize=14)

    # Add simulation details as a subtitle below the title and above the plot and above the plot
    simulation_info = (
        f"[$\\mu$] = {system_config.service_rate}, "
        f"[$\\lambda$] = {system_config.arrival_rate}, "
        f"[$t$] = {system_config.user_request_time}, "
        f"[$k$] = {system_config.number_of_servers}"
    )
    plt.title(simulation_info, fontsize=10, loc='center')

    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.plot(x, theoretical_utils, label='Theoretical Utils', color='green', marker='o')
    ax2.set_ylabel("Utilization")
    ax2.legend(loc='upper right')

    fig.tight_layout()

    figure_name = f"simulation_s{system_config.service_rate}_a{system_config.arrival_rate}_t{system_config.user_request_time}_k{system_config.number_of_servers}"
    figure_path = f"{FIGURE_FOLDER}{figure_name}.png"
    plt.savefig(figure_path)
    plt.close()


