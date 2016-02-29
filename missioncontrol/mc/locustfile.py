from locust import HttpLocust, TaskSet, task
import random
import random
import json

class UserBehavior(TaskSet):
    def on_start(self):
        pass
        #self.login()

    def login(self):
        pass
        self.client.post("/login", {"username":"ellen_key", "password":"education"})

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def group_graph(self):
        self.client.get("/show/graph/methane")

    @task(3)
    def post_sample(self):
                 
        sample = { 'x' : random.randint(1,29), 'y' : random.randint(1,19), 'team': str(random.randint(1,10)), 'methane': random.random(), 'temperature': random.random(), 'humidity': random.random() }

        rv = self.client.post('/api/sample', json=sample)

    @task(4)
    def static(self):
        self.client.get("/static/badge.png")

    @task(5)
    def static(self):
        self.client.get("/static/graphs/methane_group_2.png")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
