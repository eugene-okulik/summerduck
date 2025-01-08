from locust import task, HttpUser, between
import random


class ApiUser(HttpUser):
    """
    HOST: http://167.172.172.115:52353
    """

    wait_time = between(1, 5)  # wait time between requests

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})

    @task(1)
    def get_all_objects(
        self,
    ):
        """
        GET /object
        Retrieve a list of all objects
        """
        self.client.get("/object")

    @task(3)
    def get_object_by_id(
        self,
    ):
        """
        GET /object/<id>
        Retrieve a single object by id
        """
        random_id = random.choice(
            [
                2250,
                2251,
                2252,
                2253,
                2254,
                2255,
                2256,
                2257,
                2258,
                2259,
            ]
        )
        self.client.get(f"/object/{random_id}")
