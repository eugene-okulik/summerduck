import requests
import pytest
import allure


@pytest.fixture()
def num():
    return 3


@allure.feature('Posts')
@allure.story('Manipulate posts')
def test_delete(new_post_id):
    requests.delete(f'https://jsonplaceholder.typicode.com/posts/{new_post_id}')


@allure.feature('Example')
@allure.story('Print')
def test_num(num):
    print(num)
