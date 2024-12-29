import pytest
from decorators import log_test_details, apply_decorator_to_all_tests


@apply_decorator_to_all_tests(log_test_details)
@pytest.mark.usefixtures("start_testing")
@pytest.mark.usefixtures("before_test")
class TestApiRequests:

    @pytest.mark.critical
    def test_get_all_objects(
        self,
        api_client,
    ):
        api_client.get_all_objects()
        api_client.check_that_status_is_200()
        api_client.check_that_data_is_list()

    @pytest.mark.parametrize(
        "object_id, expected_status_code",
        [
            ("create_new_object", 200),
            ("non_existing_id", 404),
        ],
    )
    @pytest.mark.medium
    def test_get_object_by_id(
        self,
        api_client,
        create_and_cleanup_object,
        object_id,
        expected_status_code,
    ):
        api_client.get_object_by_id(object_id)
        api_client.check_that_status_is(expected_status_code)

    @pytest.mark.parametrize(
        "data, name, expected_status_code",
        [
            ({}, "", 200),
            ({}, "User", 200),
            ("fake_data", "", 200),
            ("fake_data", "User", 200),
            ([], "User", 400),
            ("fake_data", [], 400),
            ([], [], 400),
        ],
    )
    def test_post_object(
        self,
        api_client,
        fake_data,
        data,
        name,
        expected_status_code,
    ):
        # Create an fake data if data is not provided
        data = fake_data if data == "fake_data" else data

        # Create an object
        api_client.post_object(
            data=data,
            name=name,
        )
        api_client.check_that_status_is(expected_status_code)

    @pytest.mark.parametrize(
        "object_id, data, name, expected_status_code",
        [
            ("create_object", {}, "", 200),
            ("create_object", {}, "User", 200),
            ("create_object", "fake_data", "", 200),
            ("create_object", "fake_data", "User", 200),
            (NON_EXISTING_ID, "fake_data", "User", 404),
            ("create_object", [], "User", 400),
            ("create_object", "fake_data", [], 400),
            ("create_object", [], [], 400),
        ],
    )
    def test_put_object_by_id(
        self,
        api_client,
        create_and_cleanup_object,
        fake_data,
        object_id,
        data,
        name,
        expected_status_code,
    ):
        # Get object_id if it is not provided
        object_id = (
            create_and_cleanup_object if object_id == "create_object" else object_id
        )

        # Create an fake data if data is not provided
        data = fake_data if data == "fake_data" else data

        # Put object by id
        api_client.put_object_by_id(
            id=object_id,
            data=data,
            name=name,
        )
        api_client.check_that_status_is(expected_status_code)

    @pytest.mark.parametrize(
        "object_id, data, name, expected_status_code",
        [
            (
                "create_object",
                "fake_data",
                "Patched User",
                200,
            ),
            ("create_object", "fake_data", "", 200),
            ("create_object", {}, "Patched User", 200),
            ("create_object", {}, "", 400),
            ("create_object", [], "Patched User", 200),
            ("create_object", "fake_data", [], 200),
            ("create_object", [], [], 400),
            (NON_EXISTING_ID, "fake_data", "User", 404),
        ],
    )
    def test_patch_object_by_id(
        self,
        api_client,
        create_and_cleanup_object,
        fake_data,
        object_id,
        data,
        name,
        expected_status_code,
    ):
        # Get object_id if it is not provided
        object_id = (
            create_and_cleanup_object if object_id == "create_object" else object_id
        )

        # Create an fake data if data is not provided
        data = fake_data if data == "fake_data" else data

        api_client.patch_object_by_id(
            id=object_id,
            data=data,
            name=name,
        )
        api_client.check_that_status_is(expected_status_code)

    def test_delete_object(
        self,
        api_client,
        created_object,
    ):
        api_client.delete_object_by_id(created_object)
        api_client.check_that_status_is_200()
