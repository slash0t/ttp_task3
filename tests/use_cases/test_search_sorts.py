from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_SEARCH = "https://moe-online.ru/search"
SEARCH_QUERY = "погода"


def parse_news_date(raw: str) -> datetime:
    raw = raw.strip().lower()

    if "сегодня" not in raw and "вчера" not in raw:
        return datetime.strptime(raw, "%d.%m.%Y %H:%M")

    time_part, day_word = [p.strip() for p in raw.split(",", 1)]
    hour, minute = map(int, time_part.split(":"))

    today = datetime.today()

    if "сегодня" in day_word:
        date_obj = today.date()
    elif "вчера" in day_word:
        date_obj = (today - timedelta(days=1)).date()
    else:
        raise ValueError(f"Неизвестный формат даты: {raw}")

    return datetime(
        date_obj.year, date_obj.month, date_obj.day, hour, minute
    )


def test_search_sort_by_chronology(driver):
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

    SORT_BUTTON = (
        By.XPATH,
        "//label[contains(text(), 'хронологии')]"
    )

    RESULT_DATES = (
        By.CSS_SELECTOR,
        "div.inform_top_line span.time"
    )

    search_input = wait.until(
        EC.visibility_of_element_located(SEARCH_INPUT)
    )
    search_button = wait.until(
        EC.element_to_be_clickable(SEARCH_BUTTON)
    )

    search_input.clear()
    search_input.send_keys(SEARCH_QUERY)
    search_button.click()

    wait.until(
        EC.presence_of_all_elements_located(RESULT_DATES)
    )

    sort_button = wait.until(
        EC.element_to_be_clickable(SORT_BUTTON)
    )
    sort_button.click()

    wait.until(
        EC.presence_of_all_elements_located(RESULT_DATES)
    )

    date_elements = driver.find_elements(*RESULT_DATES)
    assert len(date_elements) > 0

    parsed_dates = []
    for el in date_elements:
        raw_date = el.text.strip()
        if raw_date:
            parsed_dates.append(parse_news_date(raw_date))

    sorted_desc = sorted(parsed_dates, reverse=True)

    assert parsed_dates == sorted_desc
