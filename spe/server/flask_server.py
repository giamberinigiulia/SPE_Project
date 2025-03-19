import os
import time
from flask import Flask, jsonify
import numpy as np
from scipy import signal

# from server.delay_analyzer import DelayAnalyzer
from eval import process_log
from spe.server.cpubound_task import CPUBoundTask
# from server.plot_generator import PlotGenerator

# create a pool of processes
from multiprocessing import Pool

app = Flask(__name__)

@app.route('/', methods=['GET'])
def process_task():
    rng = np.random.default_rng(42)
    delay = rng.exponential(1.0 / 10) # <---- mu_value

    CPUBoundTask.run(delay)

    return jsonify({"message": "Task completed", "duration": delay})

@app.route('/eval', methods=['GET'])
def eval_simulation():
    """Loggin the end of the i-th simulation"""
    print("Evaluation of usage")
    eval = process_log("access.log", "workers_usage.csv")
    return jsonify({
        "message": "Evaluation of usage",
        "eval": eval
    })

@app.route('/end', methods=['GET'])
def end_server():
    """End the server and clean up workers"""
    #os.kill(os.getppid(), signal.SIGINT)
    return jsonify({
        "message": "Server ended",
    })

if __name__ == '__main__':
    app.run()