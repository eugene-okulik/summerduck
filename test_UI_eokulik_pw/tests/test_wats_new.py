from test_UI_eokulik_pw.pages.whats_new_page import WhatsNew
from test_UI_eokulik_pw.pages.promo_page import PromoPage


def test_button(page):
    whats_new_page = WhatsNew(page)
    whats_new_page.open()
    whats_new_page.click_shop_the_yoga_button()
    whats_new_page.check_that_correct_url_is_opened()
    promo_page = PromoPage(page)
    promo_page.page_has_correct_title('New Luma Yoga Collection')
