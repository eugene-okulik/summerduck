import requests
import allure

from test_api_eokuik.endpoints.endpoint import Endpoint


class UpdatePost(Endpoint):

    @allure.step('Update a post')
    def make_changes_in_post(self, post_id, payload, headers=None):
        headers = headers if headers else self.headers
        self.response = requests.put(
            f'{self.url}/{post_id}',
            json=payload,
            headers=headers
        )
        self.json = self.response.json()
        return self.response
