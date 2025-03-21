# TODO: remove in the final version
# Just a simple script to check the theoretical values

from spe.argument_parser import Config
from spe.utils.metric import compute_theoretical_metrics


config = Config(
    service_rate=5.0,
    arrival_rate=10.0,
    user_range=range(1, 11),  # Number of servers (c)
    user_request_time=60,
    number_of_servers=4       # c = K
)

metrics = compute_theoretical_metrics(config)
for metric in metrics:
    print(f"Avg Response Time: {metric.avg_response_time}, Utilization: {metric.utilization}")