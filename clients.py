#invoke 127.0.0.1:5000 for 50 times

import requests

for i in range(10):
    response = requests.get('http://127.0.0.1:5000/')
    print(i)
