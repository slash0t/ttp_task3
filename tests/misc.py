import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clear_page(driver):
    wait = WebDriverWait(driver, 15)
    time.sleep(10)
    close_cookies(driver, wait)
    close_notify(driver, wait)

def close_cookies(driver, wait):
    BUTTON = (
        By.CSS_SELECTOR,
        "button.cookie_btn"
    )

    wait.until(
        EC.presence_of_all_elements_located(BUTTON)
    )
    elements = driver.find_elements(*BUTTON)

    if len(elements) == 0:
        return

    wait = WebDriverWait(driver, 15)

    button = wait.until(
        EC.element_to_be_clickable(BUTTON)
    )
    button.click()


def close_notify(driver, wait):
    BUTTON = (
        By.CSS_SELECTOR,
        "button#onesignal-slidedown-cancel-button"
    )

    wait.until(
        EC.presence_of_all_elements_located(BUTTON)
    )
    elements = driver.find_elements(*BUTTON)

    if len(elements) == 0:
        return

    wait = WebDriverWait(driver, 15)

    button = wait.until(
        EC.element_to_be_clickable(BUTTON)
    )
    button.click()
