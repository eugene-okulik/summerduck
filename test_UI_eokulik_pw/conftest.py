from playwright.sync_api import BrowserContext

import pytest
from test_UI_eokulik_pw.pages.sign_in_page import SignIn


@pytest.fixture()
def sign_in_page(page):
    return SignIn(page)


@pytest.fixture()
def page(context: BrowserContext, playwright):
    playwright.selectors.set_test_id_attribute("id")
    page = context.new_page()
    page.set_viewport_size({'width': 1920, 'height': 1080})
    return page


# @pytest.fixture
# def page(playwright):
#     playwright.selectors.set_test_id_attribute("id")
#     browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
#     context = browser.new_context(no_viewport=True)
#     # context = browser.new_context(viewport={'width': 300, 'height': 300})
#     new_page: Page = context.new_page()
#     yield new_page
#     new_page.close()
