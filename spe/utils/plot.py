from typing import List

import matplotlib.pyplot as plt
import numpy as np

from spe.utils.metrics import Metrics


def save_metrics_plot(client_count_range: range, theoretical_arts: List[float], theoretical_utils: List[float], system_metrics: Metrics, figure_name: str) -> None:
    avg_response_times = system_metrics.avg_response_times
    upper_bounds = system_metrics.upper_bounds
    lower_bounds = system_metrics.lower_bounds

    bar_width = 0.35
    x = np.arange(client_count_range.start, client_count_range.stop)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.bar(x - bar_width / 2, theoretical_arts, bar_width,
            label='Theoretical ARTs', color='skyblue', edgecolor='black', alpha=1)
    ax1.bar(x + bar_width / 2, system_metrics.avg_response_times, bar_width,
            label='Measured ARTs', color='orange', edgecolor='black', alpha=1)

    # Calculate and add error bars for confidence intervals
    error = [avg_response_times[i] - lower_bounds[i] for i in range(len(avg_response_times))]
    ax1.errorbar(x + bar_width / 2, avg_response_times, yerr=[error, [upper_bounds[i] - avg_response_times[i] for i in range(
        len(avg_response_times))]], fmt='none', ecolor='black', capsize=5, label='Confidence Interval')

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
