from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def load_homepage(self):
        self.client.get("/")  # Adjust this to target the API or specific Django views
