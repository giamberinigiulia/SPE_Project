import threading
import time

class CPUBoundTask:
    @staticmethod
    def run(duration):
        # Simulate a CPU-bound task. Fibonacci serie
        n = 70
        end_time = time.time() + duration
        while time.time() < end_time:
            x = fibonacci(n, end_time)
            print(x)

def fibonacci(n, end_time):
        if time.time() >= end_time: return n
        if n <= 1:
            return n
        else:
            return fibonacci(n-1, end_time) + fibonacci(n-2, end_time)