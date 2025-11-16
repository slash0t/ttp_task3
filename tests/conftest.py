import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tests import settings


@pytest.fixture
def driver():
    options = Options()
    if not settings.BROWSER_SHOWN:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
