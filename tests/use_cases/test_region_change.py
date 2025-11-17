from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_MAIN = "https://moe-online.ru/"


def test_region_switch_changes_city_label(driver):
    driver.get(URL_MAIN)
    wait = WebDriverWait(driver, 15)

    CURRENT_REGION = (
        By.CSS_SELECTOR,
        "div.select-city:nth-child(1) > div:nth-child(1) > a:nth-child(1) > span:nth-child(1)"
    )

    REGION_LIST_OPEN = (
        By.CSS_SELECTOR,
        "div.select-city:nth-child(1) > div:nth-child(1)"
    )

    REGION_LIST_ITEMS = (
        By.CSS_SELECTOR,
        "div.select-city:nth-child(1) > ul:nth-child(2) > li"
    )

    current_region_el = wait.until(
        EC.visibility_of_element_located(CURRENT_REGION)
    )
    current_region_name = current_region_el.text.strip()
    current_region_name = current_region_name.split(" ")[-1]
    assert current_region_name

    region_list_open = wait.until(
        EC.visibility_of_element_located(REGION_LIST_OPEN)
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_list_open)
    region_list_open.click()

    def region_list_is_loaded(driver_):
        items = driver_.find_elements(*REGION_LIST_ITEMS)
        return len(items) > 0

    assert wait.until(region_list_is_loaded)

    region_items = driver.find_elements(*REGION_LIST_ITEMS)

    new_region_el = None
    new_region_name = None

    for item in region_items:
        text = item.text.strip()
        if text and text != current_region_name:
            new_region_el = item
            new_region_name = text
            break

    assert new_region_el is not None

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", new_region_el)
    new_region_el.click()

    wait.until(
        EC.visibility_of_element_located(CURRENT_REGION)
    )

    final_region_text = driver.find_element(*CURRENT_REGION).text.strip().split(" ")[-1]
    assert final_region_text == new_region_name
    assert final_region_text != current_region_name
