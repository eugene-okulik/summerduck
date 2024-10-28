import logging
import pytest
from faker import Faker
from datetime import date
from homework.daria_summerduck.Lesson_18.api_requests import ApiClient

# Constants for tests
DEFAULT_NAME = "User"
NON_EXISTING_ID = 123


# --------------------- Fixtures ---------------------


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


# --------------------- Helper functions ---------------------


def generate_fake_data():
    # Generate fake data
    fake = Faker()
    data = fake.simple_profile()
    if isinstance(data.get("birthdate"), date):
        data["birthdate"] = data["birthdate"].isoformat()

    return data


def create_object(
    data=None,
    name=DEFAULT_NAME,
):
    api_client = ApiClient()
    data = data or generate_fake_data()
    response = api_client.post_object(data=data, name=name)
    assert response.status_code == 200, "Failed to create object"
    return response.json()["id"]


# --------------------- Test Class---------------------


@pytest.mark.usefixtures("cleanup_test_objects")
class TestApiRequests:

    def test_get_all_objects(
        self,
        api_client,
    ):
        response = api_client.get_all_objects()
        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)
        logging.info("PASSED: All objects retrieved successfully")

    @pytest.mark.parametrize(
        "description, object_id, expected_status_code",
        [
            ("Existing object", "", 200),
            ("Not existing object", NON_EXISTING_ID, 404),
        ],
    )
    def test_get_object_by_id(
        self,
        api_client,
        description,
        object_id,
        expected_status_code,
    ):
        if description == "Existing object":
            object_id = create_object()
        response = api_client.get_object_by_id(object_id)
        assert (
            response.status_code == expected_status_code
        ), f"Expected {expected_status_code} for {description}, but got {response.status_code}"

    @pytest.mark.parametrize(
        "description, data, name, expected_status_code",
        [
            ("empty data and name", {}, "", 400),
            ("empty data", {}, "User", 400),
            ("empty name", "fake_data", "", 400),
            ("valid data and name", "fake_data", "User", 200),
        ],
    )
    def test_post_object(
        self,
        api_client,
        description,
        data,
        name,
        expected_status_code,
    ):
        data = generate_fake_data() if data == "fake_data" else data

        # Create an object
        post_object_response = api_client.post_object(
            data=data,
            name=name,
        )
        assert post_object_response.status_code == expected_status_code, (
            f"Expected {expected_status_code} for creating object with {description},"
            f" but got {post_object_response.status_code}"
        )
        logging.info(f"PASSED: {description} Object created successfully")

    @pytest.mark.parametrize(
        "description, object_id, data, name, expected_status_code",
        [
            ("empty data and name", "create_object", {}, "", 400),
            ("empty data", "create_object", {}, "User", 400),
            ("empty name", "create_object", "fake_data", "", 400),
            ("valid data and name", "create_object", "fake_data", "User", 200),
            ("not existing id", NON_EXISTING_ID, "fake_data", "User", 404),
        ],
    )
    def test_put_object_by_id(
        self,
        api_client,
        description,
        object_id,
        data,
        name,
        expected_status_code,
    ):
        # Get object_id if it is not provided
        object_id = create_object() if object_id == "create_object" else object_id
        data = generate_fake_data() if data == "fake_data" else data

        put_object_response = api_client.put_object_by_id(
            id=object_id,
            data=data,
            name=name,
        )
        assert put_object_response.status_code == expected_status_code, (
            f"Expected {expected_status_code} for updating object with {description},"
            f" but got {put_object_response.status_code}"
        )
        logging.info(f"PASSED: {description} Object updated successfully")

    @pytest.mark.parametrize(
        "description, object_id, data, name, expected_status_code",
        [
            ("valid data and name", "create_object", "fake_data", "Patched User", 200),
            ("valid data and empty name", "create_object", "fake_data", "", 200),
            ("empty data and valid name", "create_object", {}, "Patched User", 200),
            ("empty data and empty name", "create_object", {}, "", 400),
        ],
    )
    def test_patch_object_by_id(
        self,
        api_client,
        description,
        object_id,
        data,
        name,
        expected_status_code,
    ):
        # Create an object
        object_id = create_object()

        data = generate_fake_data() if data == "fake_data" else data

        patch_object_response = api_client.patch_object_by_id(
            id=object_id,
            data=data,
            name=name,
        )
        assert patch_object_response.status_code == expected_status_code, (
            f"Expected {expected_status_code} for patching object with {description},"
            f" but got {patch_object_response.status_code}"
        )

    def test_delete_object(
        self,
        api_client,
    ):
        # Create an object
        object_id = create_object()
        # Delete the object
        delete_object_response = api_client.delete_object_by_id(object_id)
        assert delete_object_response.status_code == 200
        logging.info("PASSED: Object deleted successfully")
