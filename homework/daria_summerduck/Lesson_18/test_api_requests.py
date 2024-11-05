import logging
import pytest

# Constants for tests
NON_EXISTING_ID = 123


@pytest.mark.usefixtures("cleanup_test_objects")
@pytest.mark.usefixtures("start_testing")
@pytest.mark.usefixtures("before_test")
class TestApiRequests:

    @pytest.mark.critical
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
    @pytest.mark.medium
    def test_get_object_by_id(
        self,
        api_client,
        api_object,
        object_id,
        description,
        expected_status_code,
    ):
        if description == "Existing object":
            object_id = api_object["id"]
        response = api_client.get_object_by_id(object_id)
        assert (
            response.status_code == expected_status_code
        ), f"Expected {expected_status_code} for {description}, but got {response.status_code}"
        logging.info(f"PASSED: {description} Object retrieved successfully")

    @pytest.mark.parametrize(
        "description, data, name, expected_status_code",
        [
            ("empty data and empty name", {}, "", 200),
            ("empty data and valid name", {}, "User", 200),
            ("valid data and empty name ", "fake_data", "", 200),
            ("valid data and valid name", "fake_data", "User", 200),
            ("invalid data and valid name", [], "User", 400),
            ("valid data and invalid name", "fake_data", [], 400),
            ("invalid data and invalid name", [], [], 400),
        ],
    )
    def test_post_object(
        self,
        api_client,
        fake_data,
        description,
        data,
        name,
        expected_status_code,
    ):
        data = fake_data if data == "fake_data" else data

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
            ("empty data and empty name", "create_object", {}, "", 200),
            ("empty data and valid name", "create_object", {}, "User", 200),
            ("valid data and empty name", "create_object", "fake_data", "", 200),
            ("valid data and valid name", "create_object", "fake_data", "User", 200),
            ("not existing id", NON_EXISTING_ID, "fake_data", "User", 404),
            ("invalid data and valid name", "create_object", [], "User", 400),
            ("valid data and invalid name", "create_object", "fake_data", [], 400),
            ("invalid data and invalid name", "create_object", [], [], 400),
        ],
    )
    def test_put_object_by_id(
        self,
        api_client,
        api_object,
        fake_data,
        description,
        object_id,
        data,
        name,
        expected_status_code,
    ):
        # Get object_id if it is not provided
        object_id = api_object["id"] if object_id == "create_object" else object_id
        data = fake_data if data == "fake_data" else data

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
            (
                "valid data and valid name",
                "create_object",
                "fake_data",
                "Patched User",
                200,
            ),
            ("valid data and empty name", "create_object", "fake_data", "", 200),
            ("empty data and valid name", "create_object", {}, "Patched User", 200),
            ("empty data and empty name", "create_object", {}, "", 400),
            ("invalid data and valid name", "create_object", [], "Patched User", 200),
            ("valid data and invalid name", "create_object", "fake_data", [], 200),
            ("invalid data and invalid name", "create_object", [], [], 400),
            ("not existing id", NON_EXISTING_ID, "fake_data", "User", 404),
        ],
    )
    def test_patch_object_by_id(
        self,
        api_client,
        api_object,
        fake_data,
        description,
        object_id,
        data,
        name,
        expected_status_code,
    ):
        # Create an object
        object_id = api_object["id"] if object_id == "create_object" else object_id

        data = fake_data if data == "fake_data" else data

        patch_object_response = api_client.patch_object_by_id(
            id=object_id,
            data=data,
            name=name,
        )
        assert patch_object_response.status_code == expected_status_code, (
            f"Expected {expected_status_code} for patching object with {description},"
            f" but got {patch_object_response.status_code}"
        )
        logging.info(f"PASSED: {description} Object patched successfully")

    def test_delete_object(
        self,
        api_client,
        api_object,
    ):
        # Delete the object
        delete_object_response = api_client.delete_object_by_id(api_object["id"])
        assert delete_object_response.status_code == 200
        logging.info("PASSED: Object deleted successfully")
