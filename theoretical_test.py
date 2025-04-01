# TODO: remove in the final version
# Just a simple script to check the theoretical values

import numpy as np
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
print(type(metrics))
for metric in metrics:
    print(f"Avg Response Time: {metric.avg_response_time}, Utilization: {metric.utilization}")

N = 5
arrival_rate = 10.0
service_rate = 5.0
c = 2
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

print("Q matrix:")
print(Q)