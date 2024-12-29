import logging
import pytest
from faker import Faker
from datetime import date
from homework.daria_summerduck.Lesson_18.api_requests import ApiClient


@pytest.fixture()
def api_client():
    return ApiClient()


@pytest.fixture(scope="class")
def start_testing():
    logging.info("Start testing")
    yield
    logging.info("Testing completed")


@pytest.fixture(scope="function")
def before_test():
    logging.info("before test")
    yield
    logging.info("after test")


@pytest.fixture()
def fake_data():
    # Generate fake data
    fake = Faker()
    data = fake.simple_profile()
    if isinstance(data.get("birthdate"), date):
        data["birthdate"] = data["birthdate"].isoformat()
    return data


@pytest.fixture(scope="function")
def create_and_cleanup_object(fake_data, data=None, name="User"):
    non_existing_id = 123456789

    api_client = ApiClient()
    data = data or fake_data

    # Create the object
    response = api_client.post_object(data=data, name=name)
    assert response.status_code == 200, "Failed to create object"
    created_object_id = response.json()["id"]
    logging.info(f"Test object {created_object_id} created successfully")

    # Provide the created object ID to the test
    yield created_object_id

    # Cleanup: Delete created object
    api_client.delete_object_by_id(created_object_id)
    logging.info(
        f"Test objects {created_object_id} created by the test have been cleaned up successfully"
    )


@pytest.fixture()
def created_object(
    fake_data,
    data=None,
    name="User",
):
    api_client = ApiClient()
    data = data or fake_data
    response = api_client.post_object(data=data, name=name)
    assert response.status_code == 200, "Failed to create object"
    logging.info(f"Test object {response.json()['id']} created successfully")
    return response.json()["id"]
