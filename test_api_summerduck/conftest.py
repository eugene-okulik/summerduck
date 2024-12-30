import logging
import pytest
from typing import Generator
from faker import Faker
from datetime import date
from test_api_summerduck.endpoints.api_requests import ApiClient


@pytest.fixture()
def api_client():
    return ApiClient()


@pytest.fixture(scope="class")
def start_testing(
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    """Fixture to start testing"""
    logging.info(f"Start testing: {request.node.name}")
    yield
    logging.info(f"Testing completed: {request.node.name}")


def __fake_data() -> dict:
    """Generate fake data"""
    fake = Faker()
    data = fake.simple_profile()
    if isinstance(data.get("birthdate"), date):
        data["birthdate"] = data["birthdate"].isoformat()
    return data


@pytest.fixture()
def data(
    request: pytest.FixtureRequest,
) -> Generator[dict, None, None]:
    """Fixture to generate fake data"""
    data = request.param
    if data == "FAKE_DATA":
        data = __fake_data()
    else:
        data = request.param
    yield data


@pytest.fixture()
def object_id(
    request: pytest.FixtureRequest,
    data=None,
    name="User",
) -> Generator[int, None, None]:
    """Fixture to create an object and return its ID. Clean up after the test"""
    object_id = request.param
    api_client = ApiClient()

    # Handle special cases
    if object_id == "NON_EXISTING_ID":
        object_id = 1234567890

    elif object_id == "GENERATE_NEW_ID":
        # Create the object
        data = data or __fake_data()
        response = api_client.post_object(data=data, name=name)
        assert response.status_code == 200, "Failed to create test object"
        object_id = response.json()["id"]

    # Provide the created object ID to the test
    yield object_id

    # Tear down: Delete created object
    if object_id != 1234567890:
        api_client.delete_object_by_id(object_id)


@pytest.fixture()
def created_object(
    data=None,
    name="User",
) -> int:
    """Fixture to create an object and return its ID"""
    api_client = ApiClient()
    data = data or __fake_data()

    response = api_client.post_object(data=data, name=name)
    assert response.status_code == 200, "Failed to create test object"
    return response.json()["id"]


@pytest.fixture()
def log_test_info(
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    """Fixture to log test information"""
    logging.info(f"Starting test: {request.node.name}")
    logging.info(
        f"Test parameters: {request.node.callspec.params if hasattr(request.node, 'callspec') else 'No parameters'}"
    )
    yield
    logging.info(f"Finished test: {request.node.name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo,
) -> Generator[None, None, None]:
    """Hook to log test status"""
    outcome = yield
    result = outcome.get_result()
    if result.when == "call":
        logging.info(f"Test status: {result.outcome}")
