import platform
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.quit()


def get_modifier_key():
    """
    Returns the appropriate modifier key based on the operating system.
    """
    return Keys.COMMAND if platform.system().lower() == "darwin" else Keys.CONTROL


def test_demoblaze_add_to_cart(driver):
    """
    Demoblaze Add-to-Cart Test:
    1. Open the main page.
    2. Open product details in a new tab.
    3. Add the product to the cart.
    4. Close the product tab.
    5. Verify the product is present in the cart.
    """
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.demoblaze.com/index.html")
    
    # Wait for and select the product link (first product)
    product_link = wait.until(
        EC.presence_of_element_located((By.XPATH, '(//a[@href="prod.html?idp_=1"])[1]'))
    )
    
    # Open product details in a new tab using the proper modifier key
    modifier_key = get_modifier_key()
    product_link.send_keys(modifier_key + Keys.RETURN)
    
    # Wait until the new tab opens and switch to it
    wait.until(EC.number_of_windows_to_be(2))
    original_window = driver.current_window_handle
    new_tab = [handle for handle in driver.window_handles if handle != original_window][0]
    driver.switch_to.window(new_tab)
    
    # Click the "Add to cart" button and wait for the alert to appear
    add_to_cart_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Add to cart")]'))
    )
    add_to_cart_btn.click()
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    
    # Close the product tab and return to the main window
    driver.close()
    driver.switch_to.window(original_window)
    
    # Open the cart page
    cart_link = wait.until(EC.element_to_be_clickable((By.ID, 'cartur')))
    cart_link.click()
    
    # Verify that the expected product is in the cart
    product_in_cart = wait.until(
        EC.presence_of_element_located((By.XPATH, '//td[contains(text(), "Samsung galaxy s6")]'))
    )
    assert product_in_cart.text == "Samsung galaxy s6", "Product not found in cart"

def test_add_to_compare(driver):
    """
    Magento Compare Products Test:
    1. Open the Bags page.
    2. Hover over the first product.
    3. Click the "Add to Compare" button.
    4. Verify the product appears in the Compare Products section.
    """
    wait = WebDriverWait(driver, 10)
    driver.get("https://magento.softwaretestingboard.com/gear/bags.html")
    
    # Wait for the first product to be present and capture its name
    first_product = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-item"))
    )
    product_name_element = first_product.find_element(By.CSS_SELECTOR, "a.product-item-link")
    product_name = product_name_element.text.strip()
    
    # Hover over the product to reveal the "Add to Compare" button
    actions = ActionChains(driver)
    actions.move_to_element(first_product).perform()
    
    # Click the "Add to Compare" button
    compare_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@title="Add to Compare"]'))
    )
    compare_button.click()
    
    # Wait for the success message and click on the compare link
    success_message = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//div[@data-ui-id="message-success"]'))
    )
    compare_link = success_message.find_element(By.XPATH, './/a[contains(@href, "catalog/product_compare/")]')
    compare_link.click()
    
    # Wait until the Compare Products section loads and verify the product is listed
    compare_section = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="table-wrapper comparison"]'))
    )
    assert product_name in compare_section.text, (
        f"Expected product '{product_name}' not found in Compare Products section."
    )
