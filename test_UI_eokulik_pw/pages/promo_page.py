from playwright.sync_api import expect
from test_UI_eokulik_pw.pages.base_page import BasePage
import allure
from test_UI_eokulik_pw.pages.locators.whats_new import Promo as Loc


class PromoPage(BasePage):
    @property
    def page_url(self):
        return self.page_url

    @page_url.setter
    def page_url(self, value):
        self.page_url = value

    @allure.step('Check that page header is correct')
    def page_has_correct_title(self, value):
        expect(self.find(Loc.PAGE_HEADER)).to_have_text(value)
