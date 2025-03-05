"""
Часть 3
№ 1
Напишите тест, который заходит на страницу 
https://www.qa-practice.com/elements/select/single_select, 
выбирает какой-нибудь вариант из Choose language, кликает Submit и проверяет, 
что в окошке с результатом отображается тот вариант, который был выбран. 

№ 2
Напишите тест, который зайдет на страницу 
https://the-internet.herokuapp.com/dynamic_loading/2, 
нажмет Start, и проверит, что на странице появляется текст "Hello World!"
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.quit()


def test_select(driver, language="Python"):
    driver.get("https://www.qa-practice.com/elements/select/single_select")
    select_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "choose_language"))
    )
    select_element.click()
    select = Select(select_element)
    select.select_by_visible_text(language)
    select_element.send_keys(Keys.ENTER)

    driver.find_element(By.NAME, "submit").click()
    result_text = (
        WebDriverWait(driver, 10)
        .until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".result-text")))
        .text
    )
    assert language == result_text


def test_dynamic_loading(driver):
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
    )
    start_button.click()
    hello_message = (
        WebDriverWait(driver, 10)
        .until(EC.visibility_of_element_located((By.ID, "finish")))
        .text
    )
    assert "Hello World!" in hello_message
