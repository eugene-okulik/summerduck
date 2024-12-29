import allure


class Endpoint:
    url = "http://167.172.172.115:52353"
    response = None
    json = None
    headers = {"Content-type": "application/json"}

    @allure.step("Check that title is the same as sent")
    def check_response_title_is_correct(self, title):
        assert (
            self.json["title"] == title
        ), f"Expected {title}, but got {self.json['title']}"

    @allure.step("Check that response is 200")
    def check_that_status_is_200(self):
        assert (
            self.response.status == 200
        ), f"Expected 200, but got {self.response.status}"

    @allure.step("Check that 400 error received")
    def check_bad_request(self):
        assert (
            self.response.status_code == 400
        ), f"Expected 400, but got {self.response.status_code}"

    @allure.step("Check that response is ...")
    def check_that_status_is(self, status):
        assert (
            self.response.status == status
        ), f"Expected {status}, but got {self.response.status}"

    def check_that_data_is_list(self, response):
        assert isinstance(
            self.response.json()["data"], list
        ), f"Expected 'data' to be a list, but got {type(response.json()['data'])}"
