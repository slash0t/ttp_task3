from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

URL_SEARCH = "https://moe-online.ru/search"
SEARCH_QUERY = "погода"   # слово, которое точно есть в новостях


def test_search_returns_non_empty_result_list(driver):
    driver.get(URL_SEARCH)
    wait = WebDriverWait(driver, 15)

    # Поле поиска
    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[type='search']"      # при необходимости замени на реальный селектор
        # например: "input[name='text']" или "input.search__input"
    )

    # Кнопка "Найти"
    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        "button[type='submit']"     # тоже можно уточнить, если у кнопки есть свой класс
        # например: "form[action*='/search'] button"
    )

    # Элементы результатов поиска (карточки новостей)
    SEARCH_RESULT_ITEMS = (
        By.CSS_SELECTOR,
        "a[href*='/news/']"         # общее, но рабочее правило: ссылки на новости
        # можно заменить на более точный селектор, если найдетcя, например: "div.search-result-item"
    )

    # 1. Ждём поле поиска и кнопку
    search_input = wait.until(
        EC.visibility_of_element_located(SEARCH_INPUT)
    )
    search_button = wait.until(
        EC.element_to_be_clickable(SEARCH_BUTTON)
    )

    # 2. Вводим запрос
    search_input.clear()
    search_input.send_keys(SEARCH_QUERY)

    # 3. Нажимаем "Найти"
    search_button.click()

    # 4. Ждём появления результатов (минимум один элемент)
    results = wait.until(
        lambda d: d.find_elements(*SEARCH_RESULT_ITEMS)
    )

    # Проверяем, что список не пустой
    assert len(results) > 0, "Список результатов поиска оказался пустым при корректном запросе"

    # 5. Дополнительно убеждаемся, что нет сообщения «Ничего не найдено»
    nothing_found_xpath = "//*[contains(text(),'Ничего не найдено')]"

    try:
        driver.find_element(By.XPATH, nothing_found_xpath)
        nothing_found_visible = True
    except NoSuchElementException:
        nothing_found_visible = False

    assert not nothing_found_visible, "Отобразилось сообщение 'Ничего не найдено' при корректном запросе"
