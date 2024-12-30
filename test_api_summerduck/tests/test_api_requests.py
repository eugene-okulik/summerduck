import pytest
from test_api_summerduck.data import api_requests


@pytest.mark.usefixtures("start_testing", "log_test_info")
class TestApiRequests:

    @pytest.mark.critical
    def test_get_all_objects(self, api_client):
        api_client.get_all_objects()
        api_client.check_that_status_is_200()
        api_client.check_that_data_is_list()

    @pytest.mark.parametrize(
        "object_id, expected_status_code",
        api_requests.get_object_by_id_params,
        indirect=["object_id"],
    )
    @pytest.mark.medium
    def test_get_object_by_id(self, api_client, object_id, expected_status_code):
        api_client.get_object_by_id(object_id)
        api_client.check_that_status_is(expected_status_code)

    # Continue from here. Update fake_data fixture
    @pytest.mark.parametrize(
        "data, name, expected_status_code",
        api_requests.post_object_params,
        indirect=["data"],
    )
    def test_post_object(self, api_client, data, name, expected_status_code):
        api_client.post_object(name, data)
        api_client.check_that_status_is(expected_status_code)

    @pytest.mark.parametrize(
        "object_id, data, name, expected_status_code",
        api_requests.put_object_by_id_params,
        indirect=["object_id", "data"],
    )
    def test_put_object_by_id(
        self, api_client, object_id, data, name, expected_status_code
    ):
        # Put object by id
        api_client.put_object_by_id(id=object_id, data=data, name=name)
        api_client.check_that_status_is(expected_status_code)

    @pytest.mark.parametrize(
        "object_id, data, name, expected_status_code",
        api_requests.patch_object_by_id_params,
        indirect=["object_id", "data"],
    )
    def test_patch_object_by_id(
        self, api_client, object_id, data, name, expected_status_code
    ):
        api_client.patch_object_by_id(object_id, data, name)
        api_client.check_that_status_is(expected_status_code)

    def test_delete_object(self, api_client, created_object):
        api_client.delete_object_by_id(created_object)
        api_client.check_that_status_is_200()
