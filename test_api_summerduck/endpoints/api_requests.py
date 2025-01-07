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
from test_api_summerduck.decorators import apply_logging_decorators
from test_api_summerduck.endpoints.endpoint import Endpoint  # Corrected import


@apply_logging_decorators
class ApiClient(Endpoint):
    fake = Faker()
    response = None  # Add this line to store the response

    @allure.step("Retrieve a list of all objects")
    def get_all_objects(
        self,
    ) -> requests.Response:
        """
        GET /object
        Retrieve a list of all objects
        """
        self.response = requests.get(f"{self.url}/object")
        print(self.response.json())
        return self.response

    @allure.step("Retrieve a single object by id")
    def get_object_by_id(
        self,
        id: int,
    ) -> requests.Response:
        """
        GET /object/<id>
        Retrieve a single object by id
        """
        self.response = requests.get(f"{self.url}/object/{id}")
        return self.response

    @allure.step("Add a new object")
    def post_object(
        self,
        name: str,
        data: dict,
    ) -> requests.Response:
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
        self.response = requests.post(
            f"{self.url}/object",
            json=body,
            headers=headers,
        )
        return self.response

    @allure.step("Update an existing object")
    def put_object_by_id(
        self,
        id: int,
        data: dict,
        name: str = "User",
    ) -> requests.Response:
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
        self.response = requests.put(
            f"{self.url}/object/{id}",
            json=body,
            headers=headers,
        )
        return self.response

    @allure.step("Partially update an existing object")
    def patch_object_by_id(
        self,
        id: int,
        data: dict | None = None,
        name: str = "Partially updated User",
    ) -> requests.Response:
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
        self.response = requests.patch(
            f"{self.url}/object/{id}",
            json=body,
            headers=headers,
        )
        return self.response

    @allure.step("Delete an object by id")
    def delete_object_by_id(
        self,
        id: int,
    ) -> requests.Response:
        """
        DELETE /object/<id>
        Delete an object by id
        """
        self.response = requests.delete(f"{self.url}/object/{id}")
        return self.response
