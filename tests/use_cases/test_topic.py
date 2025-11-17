from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

from tests.misc import clear_page

URL_MAIN = "https://moe-online.ru/news/"


@pytest.mark.parametrize(
    "url, topic_name",
    [
        (URL_MAIN + "tests-poll", "Тесты"),
        # (URL_MAIN + "shou-biznes", "Шоу-бизнес"),
        # (URL_MAIN + "people", "Люди"),
    ],
)
def test_topic_news_relevance(driver, url, topic_name):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    clear_page(driver)

    NEWS_LINKS = (
        By.CSS_SELECTOR,
        "#load_paginate > div.material-row-plitka > div:nth-child(1) > div > div > a",
    )

    TOPIC_TEXT = (
        By.CSS_SELECTOR,
        "a.rubrika",
    )

    driver.execute_script("window.scrollBy(0, 300);")
    news_link = driver.find_elements(NEWS_LINKS)
    news_link[0].click()

    wait.until(EC.visibility_of_element_located(TOPIC_TEXT))
    breadcrumbs_elements = driver.find_element(TOPIC_TEXT)
    assert breadcrumbs_elements.text == topic_name
