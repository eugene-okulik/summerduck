"""
Часть 1
Напишите программку, которая заходит на вот эту страницу: 
https://www.qa-practice.com/elements/input/simple, 
вводит какой-то текст в поле, делает submit , 
а после этого находит элемент, в котором отображается тот текст, 
который был введен и рапечатывает этот текст.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    yield chrome_driver


def test_input_text(driver, input_data="jejrfkfkfkf"):
    driver.get("https://www.qa-practice.com/elements/input/simple")
    text_string = driver.find_element(By.CSS_SELECTOR, '[type="text"]')
    text_string.send_keys(input_data)
    text_string.send_keys(Keys.ENTER)
    entered_value = driver.find_element(By.CSS_SELECTOR, ".result-text").text
    assert input_data == entered_value
