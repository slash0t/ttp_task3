from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://moe-online.ru/news/culture/1158207"


def get_reaction_count(driver, counter_locator) -> int:
    el = driver.find_element(*counter_locator)
    text = el.text.strip()
    digits_only = "".join(ch for ch in text if ch.isdigit())
    return int(digits_only) if digits_only else 0


def test_reaction_button_toggles_counter(driver):
    url = URL
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    REACTION_BUTTON = (
        By.CSS_SELECTOR,
        "div.reactions button:nth-of-type(1)"
    )

    REACTION_COUNTER = (
        By.CSS_SELECTOR,
        "div.reactions button:nth-of-type(1) span.buttons-count"
    )

    reaction_button = wait.until(
        EC.element_to_be_clickable(REACTION_BUTTON)
    )

    wait.until(EC.visibility_of_element_located(REACTION_COUNTER))

    initial_count = get_reaction_count(driver, REACTION_COUNTER)

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reaction_button)
    reaction_button.click()

    def counter_is_incremented(driver_):
        current = get_reaction_count(driver_, REACTION_COUNTER)
        return current == initial_count + 1

    assert wait.until(counter_is_incremented)

    count_after_first_click = get_reaction_count(driver, REACTION_COUNTER)

    reaction_button.click()

    def counter_is_restored(driver_):
        current = get_reaction_count(driver_, REACTION_COUNTER)
        return current == initial_count

    assert wait.until(counter_is_restored)

    count_after_second_click = get_reaction_count(driver, REACTION_COUNTER)

    assert count_after_first_click == initial_count + 1
    assert count_after_second_click == initial_count
