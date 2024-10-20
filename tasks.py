import threading
import time
"""
import math

def compute_factorial(n):
    result = math.factorial(n)
    return result

class CPUBoundTask:
    @staticmethod
    def run(duration):
        # Simulate a CPU-bound task.
        i = 0
        end_time = time.time() + duration
        while time.time() < end_time:
            i = compute_factorial(i)
            if threading.active_count() > 1:
                print("Number of actvie threads:", threading.active_count())
"""

class CPUBoundTask:
    @staticmethod
    def run(duration):
        # Simulate a CPU-bound task. Fibonacci serie
        n = 10
        end_time = time.time() + duration
        while time.time() < end_time:
            fibonacci(n)
            print(n)

def fibonacci(n):
        if n <= 1:
            return n
        else:
            return fibonacci(n-1) + fibonacci(n-2)