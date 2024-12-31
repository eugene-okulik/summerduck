import allure


class Endpoint:
    url = "http://167.172.172.115:52353"
    response = None
    json = None
    headers = {"Content-type": "application/json"}

    @allure.step("Check that title is the same as sent")
    def check_response_title_is_correct(
        self,
        title: str,
    ) -> None:
        """Check that title is the same as sent"""
        assert (
            self.json["title"] == title
        ), f"Expected {title}, but got {self.json['title']}"

    @allure.step("Check that response is 200")
    def check_that_status_is_200(
        self,
    ) -> None:
        """Check that response is 200"""
        assert (
            self.response.status_code == 200
        ), f"Expected 200, but got {self.response.status_code}"

    @allure.step("Check that 400 error received")
    def check_bad_request(
        self,
    ) -> None:
        """Check that 400 error received"""
        assert (
            self.response.status_code == 400
        ), f"Expected 400, but got {self.response.status_code}"

    @allure.step("Check that response is ...")
    def check_that_status_is(
        self,
        status: int,
    ) -> None:
        """Check that response is as expected"""
        assert (
            self.response.status_code == status
        ), f"Expected {status}, but got {self.response.status_code}"

    def check_that_data_is_list(
        self,
    ) -> None:
        """Check that 'data' is a list"""
        assert isinstance(
            self.response.json()["data"], list
        ), f"Expected 'data' to be a list, but got {type(self.response.json()['data'])}"
