import numpy as np
import requests
import argparse

def main():
    #for j in np.arange(0.5, mu + 0.5, 0.5):
        for i in range(150):
            response = requests.get(f'http://127.0.0.1:5000/')  # You can replace 10.0 with other values as needed
            print(f"Request {i + 1}: Status Code - {response.status_code}, Response - {response.json()}")

if __name__ == "__main__":
    main()