from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_SEARCH = "https://moe-online.ru/search"
SEARCH_QUERY = "погода"


def test_search_returns_non_empty_result_list(driver):
    driver.get(URL_SEARCH)
    wait = WebDriverWait(driver, 15)

    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input.search_text"
    )

    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        "button.btn-default"
    )

    SEARCH_RESULT_ITEMS = (
        By.CSS_SELECTOR,
        "div.archive-list div.material-row-list:nth-child(1)"
    )

    search_input = wait.until(
        EC.visibility_of_element_located(SEARCH_INPUT)
    )
    search_button = wait.until(
        EC.element_to_be_clickable(SEARCH_BUTTON)
    )

    wait.until(EC.visibility_of_element_located(SEARCH_INPUT))
    search_input.clear()
    search_input.send_keys(SEARCH_QUERY)

    wait.until(EC.visibility_of_element_located(SEARCH_BUTTON))
    search_button.click()

    def search_result_list(driver_):
        return driver_.find_element(*SEARCH_RESULT_ITEMS)

    result = wait.until(search_result_list )

    assert result is not None
