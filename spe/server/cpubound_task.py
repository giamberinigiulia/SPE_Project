"""
CPUBoundTask Simulation Module.

This module defines a class to simulate CPU-bound tasks by performing 
intensive computations, such as calculating Fibonacci numbers recursively.

Classes:
- `CPUBoundTask`: Provides methods to execute CPU-bound tasks.

Methods:
- `run(duration)`: Executes a CPU-bound task for a specified duration.
- `_fibonacci(n, end_time)`: Recursively calculates the nth Fibonacci number 
  with a time constraint.

Modules Used:
- `time`: Tracks the execution time to enforce the duration limit.

Usage:
This module can be used to simulate CPU-intensive workloads for testing 
or benchmarking purposes.

Example:
    from cpubound_task import CPUBoundTask
    CPUBoundTask.run(duration=5)  # Runs the task for 5 seconds
"""
import time

class CPUBoundTask:
    @staticmethod
    def run(duration):
        """
        Executes a CPU-bound task by calculating Fibonacci numbers 
        for the specified duration in seconds.
        """
        n = 70
        end_time = time.time() + duration
        while time.time() < end_time:
            x = CPUBoundTask._fibonacci(n, end_time)

    @staticmethod
    def _fibonacci(n, end_time):
        """
        Recursively calculates the nth Fibonacci number while ensuring 
        the computation stops if the current time exceeds the end_time.
        """
        if time.time() >= end_time:
            return n
        if n <= 1:
            return n
        else:
            return CPUBoundTask._fibonacci(n-1, end_time) + CPUBoundTask._fibonacci(n-2, end_time)