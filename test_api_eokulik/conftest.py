import pytest
from endpoints.create_post import CreatePost
from endpoints.update_post import UpdatePost


@pytest.fixture()
def create_post_endpoint():
    return CreatePost()


@pytest.fixture()
def update_post_endpoint():
    return UpdatePost()


@pytest.fixture()
def post_id(create_post_endpoint):
    payload = {"title": "My generic tile", "body": "my body", "userId": 1}
    create_post_endpoint.create_new_post(payload)
    yield create_post_endpoint.post_id
