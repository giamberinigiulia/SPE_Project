import time

class CPUBoundTask:
    @staticmethod
    def run(duration):
        # Simulate a CPU-bound task. Fibonacci series calculation
        n = 70  # You can adjust this value for larger computations
        inital_time = time.time()
        end_time = inital_time + duration
        while time.time() < end_time:
            x = CPUBoundTask._fibonacci(n, end_time)  # Call the private method
            print(x)
        return time.time() - inital_time

    @staticmethod
    def _fibonacci(n, end_time):
        """Calculate the nth Fibonacci number recursively."""
        if time.time() >= end_time:
            return n  # Stop if the time is up
        if n <= 1:
            return n
        else:
            return CPUBoundTask._fibonacci(n-1, end_time) + CPUBoundTask._fibonacci(n-2, end_time)