"""This module defines a class to simulate CPU-bound tasks by calculating Fibonacci numbers recursively."""
import time


class CPUBoundTask:
    @staticmethod
    def run(duration: float) -> None:
        """
        Executes a CPU-bound task by calculating Fibonacci numbers 
        for the specified duration in seconds.
        """
        n = 70
        end_time = time.time() + duration
        while time.time() < end_time:
            x = CPUBoundTask._fibonacci(n, end_time)

    @staticmethod
    def _fibonacci(n: int, end_time: float) -> int:
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
