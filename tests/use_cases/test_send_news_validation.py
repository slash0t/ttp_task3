import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

from tests.misc import clear_page

URL_SUBMIT_NEWS = "https://moe-online.ru/frontnews/add"

@pytest.mark.parametrize(
    "input_text",
    ["a", "ab", "abc", "abcd"],
)
def test_news_title_validation_short_length(driver, input_text):
    driver.get(URL_SUBMIT_NEWS)
    wait = WebDriverWait(driver, 15)
    clear_page(driver)

    TITLE_INPUT = (
        By.CSS_SELECTOR,
        "input#frontnewsTitleUser"
    )

    SUBMIT_BUTTON = (
        By.CSS_SELECTOR,
        "input.submit.frontnewsSubmitUser"
    )

    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "span.help-block.title_error"
    )

    title_input = wait.until(
        EC.visibility_of_element_located(TITLE_INPUT)
    )

    title_input.clear()
    title_input.send_keys(input_text)

    submit_button = wait.until(
        EC.element_to_be_clickable(SUBMIT_BUTTON)
    )
    wait.until(EC.visibility_of_element_located(SUBMIT_BUTTON))
    driver.execute_script("window.scrollBy(0, 1100);")
    time.sleep(2)

    submit_button.click()

    error_message = wait.until(
        EC.visibility_of_element_located(ERROR_MESSAGE)
    )

    style = error_message.get_attribute("style")
    assert "display: none" not in style
