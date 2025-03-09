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
    # Go to page
    driver.get("https://www.demoblaze.com/index.html")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//a[@href="prod.html?idp_=1"])[1]')))

    # Open new tab with product
    samsung = driver.find_element(By.XPATH, '(//a[@href="prod.html?idp_=1"])[1]')
    modifier_key = Keys.COMMAND if operation_system() == "darwin" else Keys.CONTROL
    samsung.send_keys(modifier_key + Keys.RETURN)
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])

    # Add to cart
    add_to_cart = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Add to cart")]'))
    )
    add_to_cart.click()
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    # Close new tab
    driver.close()
    driver.switch_to.window(tabs[0])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cartur')))

    # Open cart
    cart = driver.find_element(By.ID, 'cartur')
    cart.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//td[contains(text(), "Samsung galaxy s6")]')))

    # Check product in cart
    product = driver.find_element(By.XPATH, '//td[contains(text(), "Samsung galaxy s6")]')
    assert product.text == "Samsung galaxy s6", "Product not in cart"

