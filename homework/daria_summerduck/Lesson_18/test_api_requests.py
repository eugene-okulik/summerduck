import logging
import pytest
import functools
import allure

# Constants for tests
NON_EXISTING_ID = 123456789


# ------------------------ Decorators ------------------------
def log_test_details(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        test_name = func.__name__
        logging.info(f"STARTING TEST: {test_name}")
        logging.info(f"PARAMETERS: {args}, {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"PASSED: {test_name}")
            return result
        except AssertionError as e:
            logging.error(f"FAILED: {test_name} - {str(e)}")
            raise
        except Exception as e:
            logging.error(f"ERROR: {test_name} - {str(e)}")
            raise

    return wrapper


def apply_decorator_to_all_tests(decorator):
    def class_decorator(cls):
        for attr in dir(cls):
            if callable(getattr(cls, attr)) and attr.startswith("test_"):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return class_decorator


@apply_decorator_to_all_tests(log_test_details)
@pytest.mark.usefixtures("start_testing")
@pytest.mark.usefixtures("before_test")
@allure.feature("API requests")
class TestApiRequests:

    @pytest.mark.critical
    @allure.testcase("QAP-001")
    @allure.title("Get all objects")
    @allure.tag("GET")
    @allure.story("Retrieve all objects")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_objects(
        self,
        api_client,
    ):
        response = api_client.get_all_objects()
        assert (
            response.status_code == 200
        ), f"Expected status code 200 to get all objects, but got {response.status_code}"
        assert isinstance(
            response.json()["data"], list
        ), f"Expected 'data' to be a list, but got {type(response.json()['data'])}"

    @pytest.mark.parametrize(
        "description, object_id, expected_status_code",
        [
            ("Existing object", "", 200),
            ("Not existing object", NON_EXISTING_ID, 404),
        ],
    )
    @pytest.mark.medium
    @allure.testcase("QAP-002")
    @allure.title("Get object by ID")
    @allure.tag("GET")
    @allure.story("Retrieve object by ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_object_by_id(
        self,
        api_client,
        create_and_cleanup_object,
        object_id,
        description,
        expected_status_code,
    ):
        if description == "Existing object":
            object_id = create_and_cleanup_object
        response = api_client.get_object_by_id(object_id)
        assert response.status_code == expected_status_code, (
            f"Expected {expected_status_code} for {description}, "
            f"but got {response.status_code}"
        )

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
    @allure.testcase("QAP-003")
    @allure.title("Post object")
    @allure.tag("POST")
    @allure.story("Create a new object")
    @allure.severity(allure.severity_level.CRITICAL)
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
    @allure.testcase("QAP-004")
    @allure.title("Put object by ID")
    @allure.tag("PUT")
    @allure.story("Update an object by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_put_object_by_id(
        self,
        api_client,
        create_and_cleanup_object,
        fake_data,
        description,
        object_id,
        data,
        name,
        expected_status_code,
    ):
        # Get object_id if it is not provided
        object_id = (
            create_and_cleanup_object if object_id == "create_object" else object_id
        )
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
    @allure.testcase("QAP-005")
    @allure.title("Patch object by ID")
    @allure.tag("PATCH")
    @allure.story("Partially update an object by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_patch_object_by_id(
        self,
        api_client,
        create_and_cleanup_object,
        fake_data,
        description,
        object_id,
        data,
        name,
        expected_status_code,
    ):
        # Create an object
        object_id = (
            create_and_cleanup_object if object_id == "create_object" else object_id
        )

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

    @allure.testcase("QAP-006")
    @allure.title("Delete object by ID")
    @allure.tag("DELETE")
    @allure.story("Delete an object by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_object(
        self,
        api_client,
        created_object,
    ):
        # Delete the object
        delete_object_response = api_client.delete_object_by_id(created_object)
        assert (
            delete_object_response.status_code == 200
        ), f"Expected 200 for deleting object, but got {delete_object_response.status_code}"
