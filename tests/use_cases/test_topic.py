from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


URL_MAIN = "https://moe-online.ru/news/"


@pytest.mark.parametrize(
    "url, topic_name",
    [
        (URL_MAIN + "tests-poll", "Тесты"),
        (URL_MAIN + "shou-biznes", "Шоу-бизнес"),
        (URL_MAIN + "people", "Люди"),
    ],
)
def test_topic_news_relevance(driver, url, topic_name):
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    NEWS_LINKS = (
        By.CSS_SELECTOR,
        "#load_paginate > div.material-row-plitka > div:nth-child(1) > div > div > a",
    )

    TOPIC_TEXT = (
        By.CSS_SELECTOR,
        ".material-head-rubric > a:nth-child(1)",
    )

    news_link = wait.until(
        EC.presence_of_all_elements_located(NEWS_LINKS)
    )
    # news_link[0].location_once_scrolled_into_view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", news_link[0])
    news_link[0].click()

    breadcrumbs_elements = wait.until(EC.presence_of_element_located(TOPIC_TEXT))
    assert breadcrumbs_elements.text == topic_name
