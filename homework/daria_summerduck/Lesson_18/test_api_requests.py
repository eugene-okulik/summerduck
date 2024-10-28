import logging
import json
import requests

from homework.daria_summerduck.Lesson_18.api_requests import (
    ApiClient,
    get_random_object_id_from_response_json,
    generate_fake_data,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler(),  # Output logs to the console
    ],
)
logging.getLogger("faker").setLevel(logging.WARNING)


def test_get_all_objects():
    api_client = ApiClient()
    response = api_client.get_all_objects()
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
    logging.info("PASSED: All objects retrieved successfully")


def test_get_object_by_id():
    api_client = ApiClient()
    response = api_client.get_all_objects()
    object_id = get_random_object_id_from_response_json(response)
    response = api_client.get_object_by_id(object_id)
    assert response.status_code == 200
    assert response.json()["id"] == object_id
    logging.info("PASSED: Object retrieved by id successfully")


def test_get_object_by_not_existing_id():
    api_client = ApiClient()
    response = api_client.get_object_by_id(123)
    assert response.status_code == 404
    logging.info("PASSED: Object not found by not existing id")


def test_create_object():
    data = generate_fake_data()
    name = "User"
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    assert post_object_response.status_code == 200
    logging.info("PASSED: Object created successfully")


def test_create_object_with_empty_data():
    data = {}
    name = "User"
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    try:
        assert post_object_response.status_code == 400
    except Exception as error:
        if post_object_response.status_code == 200:
            logging.warning("Object created with empty data")

        if post_object_response:
            response = api_client.get_object_by_id(post_object_response.json()["id"])
            logging.warning(f"Object: {json.dumps(response.json(), indent=4)}")

        raise requests.exceptions.HTTPError("Object created with empty data") from error

    logging.info("PASSED: Object not created with empty data")


def test_create_object_with_empty_name():
    data = generate_fake_data()
    name = ""
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    try:
        assert post_object_response.status_code == 400
    except Exception as error:
        if post_object_response.status_code == 200:
            logging.warning("Object created with empty name")

        if post_object_response:
            response = api_client.get_object_by_id(post_object_response.json()["id"])
            logging.warning(f"Object: {json.dumps(response.json(), indent=4)}")

        raise requests.exceptions.HTTPError("Object created with empty data") from error

    logging.info("PASSED: Object not created with empty name")


def test_update_object():
    data = generate_fake_data()
    name = "User"
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    object_id = post_object_response.json()["id"]

    # Update the object
    data = generate_fake_data()
    name = "Updated User"
    put_object_response = api_client.put_object_by_id(
        id=object_id,
        data=data,
        name=name,
    )
    assert put_object_response.status_code == 200
    logging.info("PASSED: Object updated successfully")


def test_update_object_with_empty_data():
    data = generate_fake_data()
    name = "User"
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    object_id = post_object_response.json()["id"]

    # Update the object
    data = {}
    name = "Updated User"
    put_object_response = api_client.put_object_by_id(
        id=object_id,
        data=data,
        name=name,
    )
    try:
        assert put_object_response.status_code == 400
    except Exception as error:
        if put_object_response.status_code == 200:
            logging.warning("Object updated with empty data")

        if put_object_response:
            response = api_client.get_object_by_id(put_object_response.json()["id"])
            logging.warning(f"Object: {json.dumps(response.json(), indent=4)}")

        raise requests.exceptions.HTTPError("Object updated with empty data") from error

    logging.info("PASSED: Object not updated with empty data")


def test_update_object_with_empty_name():
    data = generate_fake_data()
    name = "User"
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    object_id = post_object_response.json()["id"]

    # Update the object
    data = generate_fake_data()
    name = ""
    put_object_response = api_client.put_object_by_id(
        id=object_id,
        data=data,
        name=name,
    )
    try:
        assert put_object_response.status_code == 400
    except Exception as error:
        if put_object_response.status_code == 200:
            logging.warning("Object updated with empty name")

        if put_object_response:
            response = api_client.get_object_by_id(put_object_response.json()["id"])
            logging.warning(f"Object: {json.dumps(response.json(), indent=4)}")

        raise requests.exceptions.HTTPError("Object updated with empty name") from error

    logging.info("PASSED: Object not updated with empty name")


def test_update_object_with_not_existing_id():
    data = generate_fake_data()
    name = "Updated User"
    api_client = ApiClient()
    put_object_response = api_client.put_object_by_id(
        id=123,
        data=data,
        name=name,
    )

    assert put_object_response.status_code == 404
    logging.info("PASSED: Object not updated with not existing id")


def test_patch_object_by_id():
    data = generate_fake_data()
    name = "User"
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    object_id = post_object_response.json()["id"]

    # Patch the object
    data = generate_fake_data()
    name = "Patched User"
    patch_object_response = api_client.patch_object_by_id(
        id=object_id,
        data=data,
        name=name,
    )
    assert patch_object_response.status_code == 200


def test_patch_object_name_by_id():
    data = generate_fake_data()
    name = "User"
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    object_id = post_object_response.json()["id"]

    # Patch the object
    name = "Patched User"
    patch_object_response = api_client.patch_object_by_id(
        id=object_id,
        name=name,
    )
    assert patch_object_response.status_code == 200


def test_patch_object_data_by_id():
    data = generate_fake_data()
    name = "User"
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    object_id = post_object_response.json()["id"]

    # Patch the object
    data = generate_fake_data()
    patch_object_response = api_client.patch_object_by_id(
        id=object_id,
        data=data,
    )
    assert patch_object_response.status_code == 200


def test_delete_object():
    data = generate_fake_data()
    name = "User"
    api_client = ApiClient()

    # Create an object
    post_object_response = api_client.post_object(
        data=data,
        name=name,
    )
    object_id = post_object_response.json()["id"]

    # Delete the object
    delete_object_response = api_client.delete_object_by_id(object_id)
    assert delete_object_response.status_code == 200
    logging.info("PASSED: Object deleted successfully")
