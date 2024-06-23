from playwright.sync_api import Page


def test_page(page: Page):
    page.goto('https://www.google.com/')
    elt = page.get_by_role('combobox')
    print(type(elt))
