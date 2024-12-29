"""
Test API: http://167.172.172.115:52353/

## Endpoints:
GET /object
Retrieve a list of all objects

GET /object/<id>
Retrieve a single object by id

POST /object
Add a new object

Fields (all required):
name: string
data: object

PUT /object/<id>
Update an existing object

Fields (all required):
name: string
data: object

PATCH /object/<id>
Partially update an existing object

Fields (required - one of):
name: string
data: object

DELETE /object/<id>
Delete an object by id

## Task:
You need to test all the functions listed in the specification
"""

import requests
import allure
from faker import Faker
from decorators import apply_decorators_to_methods
from endpoints.endpoint import Endpoint


@apply_decorators_to_methods
class ApiClient(Endpoint):
    def __init__(self):
        self.fake = Faker()

    @allure.step("Retrieve a list of all objects")
    def get_all_objects(self):
        """
        GET /object
        Retrieve a list of all objects
        """
        return requests.get(f"{self.url}/object")

    @allure.step("Retrieve a single object by id")
    def get_object_by_id(self, id: int):
        """
        GET /object/<id>
        Retrieve a single object by id
        """
        return requests.get(f"{self.url}/object/{id}")

    @allure.step("Add a new object")
    def post_object(
        self,
        name: str,
        data: dict,
    ):
        """
        POST /object
        Add a new object

        Fields (all required):
        name: string
        data: object
        """
        body = {
            "name": name,
            "data": data,
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(
            f"{self.url}/object",
            json=body,
            headers=headers,
        )
        return response

    @allure.step("Update an existing object")
    def put_object_by_id(
        self,
        id: int,
        *,
        data: dict,
        name: str = "User",
    ):
        """
        PUT /object/<id>
        Update an existing object

        Fields (all required):
        name: string
        data: object
        """
        body = {
            "name": name,
            "data": data,
        }
        headers = {"Content-Type": "application/json"}
        return requests.put(
            f"{self.url}/object/{id}",
            json=body,
            headers=headers,
        )

    @allure.step("Partially update an existing object")
    def patch_object_by_id(
        self,
        id: int,
        data: dict | None = None,
        name: str = "Partially updated User",
    ):
        """
        PATCH /object/<id>
        Partially update an existing object

        Fields (required - one of):
        name: string
        data: object
        """
        body = {}
        if name:
            body["name"] = name
        if data:
            body["data"] = data

        headers = {"Content-Type": "application/json"}
        return requests.patch(
            f"{self.url}/object/{id}",
            json=body,
            headers=headers,
        )

    @allure.step("Delete an object by id")
    def delete_object_by_id(self, id: int):
        """
        DELETE /object/<id>
        Delete an object by id
        """
        return requests.delete(f"{self.url}/object/{id}")
