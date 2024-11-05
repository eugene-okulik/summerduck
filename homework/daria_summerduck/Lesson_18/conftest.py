import logging
import pytest
from faker import Faker
from datetime import date
from homework.daria_summerduck.Lesson_18.api_requests import ApiClient


@pytest.fixture()
def api_client():
    return ApiClient()


@pytest.fixture(scope="class")
def cleanup_test_objects():
    api_client = ApiClient()
    yield
    response = api_client.get_all_objects()
    object_ids = [obj["id"] for obj in response.json()["data"]]
    for object_id in object_ids[1:]:
        api_client.delete_object_by_id(object_id)
    response = api_client.get_all_objects()
    assert len(response.json()["data"]) == 1
    logging.info("All test objects cleaned up successfully")


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


@pytest.fixture()
def api_object(
    fake_data,
    data=None,
    name="User",
):
    api_client = ApiClient()
    data = data or fake_data
    response = api_client.post_object(data=data, name=name)
    assert response.status_code == 200, "Failed to create object"
    return response.json()
