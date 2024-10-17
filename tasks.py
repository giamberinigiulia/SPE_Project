import time
import math

class CPUBoundTask:
    @staticmethod
    def run(duration):
        """Simulate a CPU-bound task."""
        x = 12345.6789
        y = 98765.4321
        z = 0
        end_time = time.time() + duration
        while time.time() < end_time:
            z += math.sqrt(x) * math.sqrt(y)
            print(z)

