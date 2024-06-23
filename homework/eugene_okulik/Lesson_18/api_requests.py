import requests


def all_posts():
    # response = requests.request('GET', 'https://jsonplaceholder.typicode.com/posts')
    response = requests.get('https://jsonplaceholder.typicode.com/posts').json()
    assert len(response) == 100, 'Not all posts returned'


def one_post():
    post_id = new_post()
    response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_id}').json()
    assert response['id'] == post_id


def post_a_post():
    body = {
        "title": "fsakjdhfkasjdhflkajsdhlkfjashdfoo",
        "body": "barasdfaskdjfhlaksdfoiwueysdhgkjashdkfjhalskdjfhasdf",
        "userId": 1
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        'https://jsonplaceholder.typicode.com/posts',
        json=body,
        headers=headers
    )
    assert response.status_code == 201, 'Status code is incorrect'
    assert response.json()['id'] == 101, 'Id is incorrect'


def new_post():
    body = {
        "title": "fsakjdhfkasjdhflkajsdhlkfjashdfoo",
        "body": "barasdfaskdjfhlaksdfoiwueysdhgkjashdkfjhalskdjfhasdf",
        "userId": 1
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        'https://jsonplaceholder.typicode.com/posts',
        json=body,
        headers=headers
    )
    return response.json()['id']


def clear(post_id):
    requests.delete(f'https://jsonplaceholder.typicode.com/posts/{post_id}')


def put_a_post():
    post_id = new_post()
    body = {
        "title": "fsakjdhfkasjdhflkajsdhlkfjashdfoo-UPD",
        "body": "barasdfaskdjfhlaksdfoiwueysdhgkjashdkfjhalskdjfhasdf-UPD",
        "userId": 1
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.put(
        f'https://jsonplaceholder.typicode.com/posts/{post_id}',
        json=body,
        headers=headers
    ).json()
    assert response['title'] == 'fsakjdhfkasjdhflkajsdhlkfjashdfoo-UPD'
    clear(post_id)


def patch_a_post():
    post_id = new_post()
    body = {
        "body": "barasdfaskdjfhlaksdfoiwueysdhgkjashdkfjhalskdjfhasdf-UPD",
        "userId": 7
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.patch(
        f'https://jsonplaceholder.typicode.com/posts/{post_id}',
        json=body,
        headers=headers
    ).json()
    print(response)
    clear(post_id)


def delete_a_post():
    post_id = new_post()
    response = requests.delete(f'https://jsonplaceholder.typicode.com/posts/{post_id}')
    print(response.json())
    print(response.status_code)


post_a_post()
