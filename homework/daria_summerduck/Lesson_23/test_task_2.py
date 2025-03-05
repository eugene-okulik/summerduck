"""
Часть 2
Напишите программу, которая зайдет на страницу 
https://demoqa.com/automation-practice-form 
и полностью заполнит форму (кроме загрузки файла) и нажмет Submit.

Небольшая особенность
Страничка эта немного кривая, иногда реклама перекрывает 
элементы и по ним невозможно кликнуть (но сейчас, смотрю, вообще реклама пропала).
Если бы это было приложение, которое мы тестируем, это был бы баг. 
Но работаем с тем, что есть. И для нас это даже плюс, нужно найти как выкрутиться.
Обойти это можно уменьшив размер экрана браузера - тогда элементы перераспределяются 
и становятся доступны. Но если реклама так и не появится, то ничего на странице не мешает. 

После отправки вам будет отображено окошко с тем что вы ввели. 
Получите со страницы содержимое этого окошка и распечатайте (выведите на экран).

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    yield chrome_driver


def test_fill_form(
    driver,
    first_name_value="Daria",
    last_name_value="Summerduck",
    email_value="daria.summerduck@gmail.com",
    gender_value="Female",
    number_value="1234567890",
    date_of_birth_value="01 January 2000",
    subjects_value="Maths",
    hobbies_value="Reading",
    current_address_value="Minsk",
    state_and_city_value="NCR Delhi",
):
    # Go to the page
    driver.get("https://demoqa.com/automation-practice-form")

    day_value, month_of_birth_value, year_value = date_of_birth_value.split(" ")

    # Locators
    first_name = driver.find_element(By.ID, "firstName")
    last_name = driver.find_element(By.ID, "lastName")
    email = driver.find_element(By.ID, "userEmail")
    gender = driver.find_element(By.XPATH, f"//label[text()='{gender_value}']")
    number = driver.find_element(By.ID, "userNumber")
    date_of_birth = driver.find_element(By.ID, "dateOfBirthInput")
    subjects = driver.find_element(By.ID, "subjectsInput")
    hobbies = driver.find_element(By.XPATH, f"//label[text()='{hobbies_value}']")
    current_address = driver.find_element(By.ID, "currentAddress")
    state = driver.find_element(By.ID, "react-select-3-input")
    city = driver.find_element(By.ID, "react-select-4-input")
    submit = driver.find_element(By.ID, "submit")

    # Fill Name, Email, Gender
    first_name.send_keys(first_name_value)
    last_name.send_keys(last_name_value)
    email.send_keys(email_value)
    gender.click()
    number.send_keys(number_value)

    # Date of birth
    date_of_birth.click()
    # wait for the year dropdown to be clickable
    year_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//select[@class="react-datepicker__year-select"]')
        )
    )
    year_dropdown.click()
    year_option = driver.find_element(
        By.XPATH,
        f'//select[@class="react-datepicker__year-select"]//option[@value="{year_value}"]',
    )
    year_option.click()
    # Select month
    month_dropdown = driver.find_element(
        By.XPATH, '//select[@class="react-datepicker__month-select"]'
    )
    month_dropdown.click()
    month_option = driver.find_element(
        By.XPATH,
        f'//select[@class="react-datepicker__month-select"]//option[text()="{month_of_birth_value}"]',
    )
    month_option.click()
    # Select day (assuming day_value can be used directly; if needed, remove any leading 0)
    day_int = str(int(day_value))
    day = driver.find_element(
        By.XPATH, f'//div[contains(@aria-label,"{month_of_birth_value} {day_int}")]'
    )
    day.click()

    # Subjects, Hobbies, Address, State and City
    subjects.send_keys(subjects_value)
    subjects.send_keys(Keys.ENTER)
    hobbies.click()
    current_address.send_keys(current_address_value)
    state_value, city_value = state_and_city_value.split(" ")
    state.send_keys(state_value)
    state.send_keys(Keys.ENTER)
    city.send_keys(city_value)
    city.send_keys(Keys.ENTER)

    # Submit the form
    submit.click()

    # Wait for the modal
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
    )

    # Get the modal content and print it
    modal_content = driver.find_element(By.CLASS_NAME, "modal-body").text
    print(modal_content)
