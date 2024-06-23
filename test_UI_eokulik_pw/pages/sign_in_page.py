from playwright.sync_api import expect
import allure
from test_UI_eokulik_pw.pages.base_page import BasePage


ERROR_MESSAGE = '//div[@role="alert"]'


class SignIn(BasePage):
    page_url = '/customer/account/login'

    @allure.step('Enter email')
    def enter_email(self, email):
        email_field = self.page.get_by_test_id('email')
        # email_field = self.find('#email')
        email_field.fill(email)

    @allure.step('Enter password')
    def enter_password(self, password):
        passw = self.find('#pass')
        passw.fill(password)

    @allure.step('Click the button')
    def click_submit_button(self):
        self.find('#send2').click()

    @allure.step('Check message')
    def check_error_message(self, message):
        # message_elt = self.find(ERROR_MESSAGE)
        expect(self.page.get_by_role("alert").first).to_have_text(message)
