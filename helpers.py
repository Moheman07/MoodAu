from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_and_click(driver, by_type, identifier, timeout=30):
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by_type, identifier))
    ).click()

def wait_for_element(driver, by_type, identifier, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by_type, identifier))
    )
