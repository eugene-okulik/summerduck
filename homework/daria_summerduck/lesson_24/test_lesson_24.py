"""
Первый тест
https://www.demoblaze.com/index.html

откройте товар в новой вкладке
Перейдите на вкладку с товаром
Добавьте товар в корзину
Закройте вкладку с товаром
На начальной вкладке откройте корзину
Убедитесь, что в корзине тот товар, который вы добавляли
Второй тест
https://magento.softwaretestingboard.com/gear/bags.html
Навести мышку на первый товар ->
кликнуть внизу карточки товара на кнопку Add to compare
-> Проверить, что товар появился слева на этой же странице в секции Compare Products
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time
import pytest
import platform

@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.quit()


def operation_system():
    return platform.system().lower()


def test_demoblaze_add_to_cart(driver):

    # Set up an explicit wait
    wait = WebDriverWait(driver, 10)

    # Go to page
    driver.get("https://www.demoblaze.com/index.html")
    wait.until(EC.presence_of_element_located((By.XPATH, '(//a[@href="prod.html?idp_=1"])[1]')))

    # Open new tab with product
    samsung = driver.find_element(By.XPATH, '(//a[@href="prod.html?idp_=1"])[1]')
    modifier_key = Keys.COMMAND if operation_system() == "darwin" else Keys.CONTROL
    samsung.send_keys(modifier_key + Keys.RETURN)
    wait.until(lambda d: len(d.window_handles) > 1)
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])

    # Add to cart
    add_to_cart = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Add to cart")]'))
    )
    add_to_cart.click()
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    # Close new tab
    driver.close()
    driver.switch_to.window(tabs[0])
    wait.until(EC.presence_of_element_located((By.ID, 'cartur')))

    # Open cart
    cart = driver.find_element(By.ID, 'cartur')
    cart.click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//td[contains(text(), "Samsung galaxy s6")]')))

    # Check product in cart
    product = driver.find_element(By.XPATH, '//td[contains(text(), "Samsung galaxy s6")]')
    assert product.text == "Samsung galaxy s6", "Product not in cart"


def test_add_to_compare(driver):

    # Set up an explicit wait
    wait = WebDriverWait(driver, 10)

    try:
        # Open the target URL
        driver.get("https://magento.softwaretestingboard.com/gear/bags.html")

        # Wait until the first product is present on the page
        first_product = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-item"))
        )

        # Retrieve the product name for later verification (adjust the selector if needed)
        product_name_element = first_product.find_element(By.CSS_SELECTOR, "a.product-item-link")
        product_name = product_name_element.text

        # Hover over the first product to reveal the additional options
        actions = ActionChains(driver)
        actions.move_to_element(first_product).perform()

        # Wait until the "Add to Compare" button is clickable (using XPath matching its text)
        add_to_cart_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@title="Add to Compare"]'))
        )

        # Click the "Add to Compare" button
        add_to_cart_button.click()

        # Wait until the Compare Products section is present (adjust selector if needed)
        compare_section_message = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-ui-id="message-success"]'))
        )
        compare_section_link = compare_section_message.find_element(By.XPATH, '//a[@href="https://magento.softwaretestingboard.com/catalog/product_compare/"]')
        compare_section_link.click()
        # Wait until the Compare Products section is updated with the product
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="table-wrapper comparison"]'))
        )

        # Verify that the product name appears in the Compare Products section
        compare_section = driver.find_element(By.XPATH, '//div[@class="table-wrapper comparison"]')
        assert product_name in compare_section.text, (
            f"Expected product '{product_name}' not found in Compare Products section."
        )
        print("Test passed: Product added to Compare Products successfully.")

    finally:
        # Close the browser
        driver.quit()
