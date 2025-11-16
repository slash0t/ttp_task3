from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_MAIN = "https://moe-online.ru/"

EXPECTED_TEXTS = [
    "Учредитель: ООО «Издательский дом «Свободная пресса»",
    "И. о. главного редактора редакции «МОЁ!»-«МОЁ! Online» — Усков Сергей Владимирович",
    "Редактор сайта «МОЁ! Online» — Екатерина Коваленко",
    "Адрес редакции: 394049 г. Воронеж, ул. Л.Рябцевой, 54",
    "Телефоны редакции: (473) 267-94-00, 264-93-98",
    "E-mail редакции: web@moe-online.ru и moe@moe-online.ru",
]


def test_footer_contains_legal_info(driver):
    driver.get(URL_MAIN)
    wait = WebDriverWait(driver, 15)

    FOOTER = (
        By.CSS_SELECTOR,
        "footer"
    )

    footer = wait.until(
        EC.visibility_of_element_located(FOOTER)
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", footer)

    footer_text = footer.text

    for piece in EXPECTED_TEXTS:
        assert piece in footer_text, f"В футере не найден ожидаемый текст: {piece!r}"
