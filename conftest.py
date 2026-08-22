from selenium import webdriver
import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from config import TOKEN


def pytest_addoption(parser):
    """Регистрация параметров командной строки"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Выбор браузера: chrome, firefox или edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск в headless режиме"
    )


@pytest.fixture(scope="session")
def browser(request):
    """
    Фикстура для запуска браузера.

    Примеры использования:
        pytest tests/ --browser=chrome
        pytest tests/ --browser=firefox --headless
        pytest tests/ --browser=edge
    """
    browser_name = request.config.getoption("--browser", default="chrome")
    headless = request.config.getoption("--headless", default=False)

    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )

    elif browser_name.lower() == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")

        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

    driver.maximize_window()
    driver.get(url="https://www.chitai-gorod.ru")
    driver.add_cookie({
   "name": "access-token",
   "value": f"Bearer {TOKEN}",
   "domain": ".chitai-gorod.ru"
})

    yield driver

    driver.quit()

