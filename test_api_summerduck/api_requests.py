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
import logging
import json
import functools
from faker import Faker

BASE_URL = "http://167.172.172.115:52353"

# ------------------------ Decorators ------------------------


def status_logging(func):
    """
    Decorator to log the status code of the response.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.debug(f"---------------- {func.__name__} ----------------")
            response = func(*args, **kwargs)
            assert (
                response.status_code == 200
            ), f"Status code is incorrect - {response.status_code}"
            logging.debug(f"response.status_code: {response.status_code}")
        except Exception as error:
            logging.warning(f"{func.__name__} failed: {error}")
        finally:
            return response

    return wrapper


def response_logging(func):
    """
    Decorator to log the response json of the response.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            logging.debug(f"response.json: {json.dumps(response.json(), indent=4)}")
        except Exception as error:
            logging.warning(f"{func.__name__} failed: {error}")
        finally:
            return response

    return wrapper


def apply_decorators_to_methods(cls):
    """
    Class decorator to apply response_logging and status_logging to all methods
    that start with "get_", "post_", "put_", "patch_", or "delete_".
    """
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and attr_name.startswith(("delete_")):
            setattr(
                cls,
                attr_name,
                status_logging(attr_value),
            )
        if callable(attr_value) and attr_name.startswith(
            (
                "get_",
                "post_",
                "put_",
                "patch_",
            )
        ):
            setattr(
                cls,
                attr_name,
                response_logging(status_logging(attr_value)),
            )
    return cls


# ------------------------ API Class ------------------------


@apply_decorators_to_methods
class ApiClient:
    BASE_URL = BASE_URL

    def __init__(self):
        self.fake = Faker()

    def get_all_objects(self):
        """
        GET /object
        Retrieve a list of all objects
        """
        return requests.get(f"{self.BASE_URL}/object")

    def get_object_by_id(self, id: int):
        """
        GET /object/<id>
        Retrieve a single object by id
        """
        return requests.get(f"{self.BASE_URL}/object/{id}")

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
            f"{self.BASE_URL}/object",
            json=body,
            headers=headers,
        )
        return response

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
            f"{self.BASE_URL}/object/{id}",
            json=body,
            headers=headers,
        )

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
            f"{self.BASE_URL}/object/{id}",
            json=body,
            headers=headers,
        )

    def delete_object_by_id(self, id: int):
        """
        DELETE /object/<id>
        Delete an object by id
        """
        return requests.delete(f"{self.BASE_URL}/object/{id}")
