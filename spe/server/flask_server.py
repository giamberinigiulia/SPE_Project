import os
import time
from flask import Flask, jsonify
import numpy as np
from scipy import signal

from spe.server.cpubound_task import CPUBoundTask
# from server.plot_generator import PlotGenerator

# create a pool of processes
from multiprocessing import Pool

app = Flask(__name__)

rng = np.random.default_rng(42)
mu = 10 # default value 

@app.route('/', methods=['GET'])
def process_task():
    delay = rng.exponential(1 / mu) # <---- mu_value
    print(f"Delay sampled: {delay}")

    CPUBoundTask.run(delay)

    return jsonify({"message": "Task completed", "duration": delay})

@app.route('/mu/', methods=['GET'])
def update_mu(mu_value):
    global mu 
    print(type(mu_value))
    mu = float(mu_value)
    print(type(mu))
    return jsonify({"message": "mu updated", "mu": mu})

@app.route('/end', methods=['GET'])
def end_server():
    """End the server and clean up workers"""
    #os.kill(os.getppid(), signal.SIGINT)
    return jsonify({
        "message": "Server ended",
    })

if __name__ == '__main__':
    app.run()