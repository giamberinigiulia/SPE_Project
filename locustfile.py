from locust import HttpUser, TaskSet, task, events
from numpy import random

class User(HttpUser):
    
    @task
    def load_home_page(self):
        self.client.get("/")

    def wait_time(self):
        return random.exponential(1/8) # change it!

