import allure


@allure.feature('Sign in')
def test_incorrect_login(sign_in_page):
    sign_in_page.open()
    sign_in_page.enter_email('sjdskd@weiur.com')
    sign_in_page.enter_password('sdoiuwkejbskd')
    sign_in_page.click_submit_button()
    sign_in_page.check_error_message(
        'The account sign-in was incorrect or your account is disabled temporarily. '
        + 'Please wait and try again later.'
    )
