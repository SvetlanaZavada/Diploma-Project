import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import time


class CatalogPage:
    """Класс реализует основные сценарии работы со страницей каталога:
    поиск и фильтрацию товаров, сортировку,
    управление избранным, добавление в корзину и переход в неё."""

    # Локаторы элементов страницы
    SEARCH_INPUT_FIELD = By.ID, "app-search"  # поле поиска
    SEARCH_BUTTON = (
        By.XPATH,  "//button[@aria-label='Найти']//span["
        "@class='chg-app-button__icon chg-app-button__icon--with-indicator']"
                   "//*[""name()='svg']")
    CART = By.CSS_SELECTOR, "button[aria-label='Корзина']"
    CART_BUTTON = (By.CSS_SELECTOR, "button[data-testid-button-header='cart']")
    CART_INDICATOR = (
        By.CSS_SELECTOR,
        ".chg-app-indicator.chg-app-indicator--m.header-controls__indicator")
    # Локаторы для карточки товара (один элемент)
    PRODUCT_CARD = By.CSS_SELECTOR, ".product-card"  # сама карточка
    # Локаторы ВНУТРИ карточки
    PRODUCT_TITLE = By.CSS_SELECTOR, ".product-card__title"  # название книги
    PRODUCT_AUTHOR = By.CSS_SELECTOR, ".product-card__subtitle"  # автор
    #  Купить
    BUY_BUTTON = By.XPATH, ".//div[contains(text(), 'Купить')]"
    CHECKOUT_BUTTON_TEXT = By.XPATH, ".//div[contains(text(), 'Оформить')]"
    # Локаторы всплывающих окон
    POPUP_CITY_BUTTON = (By.XPATH, "//div[contains(text(), 'Да, я здесь')]")
    POPUP_COOKIE_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'agreement-notice__button')]//div["
        "contains(text(), 'Понятно, закрыть')]")
    POPUP_MECHANIC_CLOSE = (By.CSS_SELECTOR,
                            "[id^='popmechanic-container'] .popmechanic-close")
    POPUP_MECHANIC_CLOSE_ALL = (By.CSS_SELECTOR, "div.popmechanic-close")

    def __init__(self, driver) -> None:
        self.driver = driver
        self.default_timeout = 30

    @allure.step("Закрыть все всплывающие окна")
    def close_all_popups(self) -> None:
        # 1. Всплывашка с городом
        try:
            button = WebDriverWait(
                self.driver, self.default_timeout).until(
                EC.element_to_be_clickable(self.POPUP_CITY_BUTTON))
            button.click()
            print("Закрыта всплывашка с городом")
        except Exception:
            pass

        # 2. Всплывашка с Cookie
        try:
            button = WebDriverWait(
                self.driver, self.default_timeout).until(
                EC.element_to_be_clickable(self.POPUP_COOKIE_BUTTON))
            button.click()
            print("Закрыта всплывашка с Cookie")
        except Exception:
            pass

        """Закрывает все всплывашки на странице"""
        # . Всплывашка popmechanic
        try:
            close_buttons = self.driver.find_elements(
                *self.POPUP_MECHANIC_CLOSE)
            for button in close_buttons:
                if button.is_displayed():
                    button.click()
                    print(" Закрыта всплывашка popmechanic")
                    break
        except Exception:
            pass
        try:
            close_buttons = self.driver.find_elements(
                *self.POPUP_MECHANIC_CLOSE_ALL)
            for button in close_buttons:
                if button.is_displayed():
                    button.click()
                    print(" Закрыта всплывашка popmechanic")
                    break
        except Exception:
            pass

        return self

    @allure.step("Закрыть все всплывающие окна через JS")
    def close_all_ads(self) -> None:
        """Закрывает всю рекламу на странице через JS"""
        self.driver.execute_script("""
            // Удаляем popmechanic
            document.querySelectorAll(
            '[id^="popmechanic"]').forEach(el => el.remove());
            document.querySelectorAll(
            '[class*="popmechanic"]').forEach(el => el.remove());
            // Убираем скролл блокировку
            document.body.style.overflow = 'auto';
        """)
        time.sleep(0.5)
        return self

    @allure.step("Посмотреть текущий url")
    def get_current_url(self) -> str:
        """Возвращает текущий URL страницы"""
        return self.driver.current_url

    @allure.step("Открыть страницу каталога")
    def open_catalog_page(self) -> "CatalogPage":
        self.driver.get("https://www.chitai-gorod.ru/catalog/books-18030")
        return self

    @allure.step("ввести запрос в строку поиска")
    def enter_query(self, query: str) -> "CatalogPage":
        enter_query = self.driver.find_element(*self.SEARCH_INPUT_FIELD)
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.element_to_be_clickable(self.SEARCH_INPUT_FIELD)
        )
        enter_query.clear()
        enter_query.send_keys(query)
        return self

    @allure.step("Начать поиск")
    def search(self) -> None:
        """
        Выполняет поиск с обработкой всплывающих окон и повторными попытками.
        """
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            try:
                # 1. Проверяем и закрываем всплывашки перед кликом
                self.close_all_popups()

                # 2. Ждем, пока кнопка станет кликабельной
                WebDriverWait(
                    self.driver, self.default_timeout).until(
                    EC.element_to_be_clickable(self.SEARCH_BUTTON)
                )

                # 3. Находим кнопку и скроллим к ней
                search_button = self.driver.find_element(*self.SEARCH_BUTTON)
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({"
                    "block: 'center', behavior: 'smooth'});",
                    search_button
                )
                time.sleep(0.5)  # Даем время на анимацию

                # 4. Пробуем кликнуть
                search_button.click()

                # 5. Ждем изменения URL
                WebDriverWait(
                    self.driver, self.default_timeout).until(
                    EC.url_contains("search?phrase=")
                )

                self.close_all_popups()

                print("✅ Поиск выполнен успешно")
                return self

            except TimeoutException as e:
                attempt += 1
                print(f"⚠️ Попытка {attempt} не удалась: {e}")

                # Закрываем всплывашки, которые могли помешать
                self.close_all_popups()

                if attempt < max_attempts:
                    wait_time = 2 * attempt
                    print(f"⏳ Повторная попытка через {wait_time} секунд...")
                    time.sleep(wait_time)
                else:
                    # делаем скриншот и выбрасываем ошибку
                    self.driver.save_screenshot(
                        f"search_error_attempt_{attempt}.png")
                    raise Exception(f"❌ Не удалось выполнить поиск после "
                                    f"{max_attempts} попыток")

        return self

    @allure.step("Получить список авторов первых 5 книг")
    def get_authors_from_books(self) -> list:
        """
        Возвращает список авторов первых 5 книг на странице.

        Returns:
            list: Список строк с именами авторов
        """
        self.close_all_popups()
        WebDriverWait(
            self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.PRODUCT_CARD))

        all_cards = self.driver.find_elements(*self.PRODUCT_CARD)
        cards = all_cards[:5]
        authors = []

        for card in cards:
            try:
                author = card.find_element(
                    *self.PRODUCT_AUTHOR).get_attribute("title")
                authors.append(author)
            except Exception:
                authors.append("Автор не указан")

        print(f"📚 Найдены авторы: {authors}")
        return authors

    @allure.step("Получить список названий первых 5 книг")
    def get_titles_from_books(self) -> list:
        """
        Возвращает список названий первых 5 книг на странице.

        Returns:
            list: Список строк с названиями книг
        """
        self.close_all_popups()
        WebDriverWait(
            self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.PRODUCT_CARD))

        all_cards = self.driver.find_elements(*self.PRODUCT_CARD)
        cards = all_cards[:5]
        titles = []

        for card in cards:
            try:
                title = card.find_element(
                    *self.PRODUCT_TITLE).get_attribute("title")
                titles.append(title)
            except Exception:
                titles.append("Название не найдено")

        print(f"📚 Найдены названия: {titles}")
        return titles

    @allure.step("посмотреть карточку")
    def view_card(self) -> None:
        first_card = self.driver.find_element(*self.PRODUCT_CARD)
        self.driver.execute_script("arguments[0].scrollIntoView("
                                   "{block: 'center', behavior: 'smooth'});",
                                   first_card)
        WebDriverWait(
            self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.PRODUCT_CARD))
        first_card.click()

    @allure.step("Добавить первую книгу в корзину")
    def add_first_book_to_cart(self) -> None:
        """
        Находит первую карточку товара и нажимает кнопку "Купить".
        """
        # 1. Находим первую карточку
        first_card = self.driver.find_element(*self.PRODUCT_CARD)
        self.driver.execute_script("arguments[0].scrollIntoView("
                                   "{block: 'center', behavior: 'smooth'});",
                                   first_card)
        WebDriverWait(
            self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.PRODUCT_CARD))
        # 2. Находим кнопку "Купить" внутри карточки
        buy_button = self.driver.find_element(*self.BUY_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView("
                                   "{block: 'center', behavior: 'smooth'});",
                                   buy_button)
        WebDriverWait(
            self.driver, self.default_timeout).until(
            EC.element_to_be_clickable(self.BUY_BUTTON)
        )
        # 3. Кликаем
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Находим кнопку "Купить"
                buy_button = self.driver.find_element(*self.BUY_BUTTON)

                # Скроллим к кнопке
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({"
                    "block: 'center', behavior: 'smooth'});",
                    buy_button
                )
                time.sleep(0.5)

                # Пробуем кликнуть
                buy_button.click()
                print("✅ Книга добавлена в корзину")
                break

            except ElementClickInterceptedException:
                print(f"⚠️ Попытка {attempt + 1}: "
                      f"кнопка перекрыта, пробую закрыть всплывашки...")
                # Закрываем всплывашки
                self.close_all_popups()
                time.sleep(1)

                if attempt == max_attempts - 1:
                    # Последняя попытка - клик через JS
                    print("🔄 Пробуем кликнуть через JS")
                    self.driver.execute_script("""
                                var buttons = document.querySelectorAll(
                                '.product-card:first-child button');
                                for (var i = 0; i < buttons.length; i++) {
                                    if (buttons[i].textContent.includes(
                                    'Купить')) {
                                        buttons[i].click();
                                        break;
                                    }
                                }
                            """)
                    print("✅ Книга добавлена через JS")

            except Exception as e:
                if attempt < max_attempts - 1:
                    print(f"⚠️ Попытка {attempt + 1} не удалась: {e}")
                    time.sleep(1)
                else:
                    raise

        # 4. Ждем, что текст изменился на "Оформить"
        WebDriverWait(
            self.driver, self.default_timeout).until(
            EC.visibility_of_element_located(self.CHECKOUT_BUTTON_TEXT)
        )
        return self

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> None:
        button_cart = self.driver.find_element(*self.CART_BUTTON)
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.element_to_be_clickable(self.CART_BUTTON)
        )
        button_cart.click()
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.url_contains("cart")
        )

    @allure.step("Получить текст кнопки первой книги в каталоге")
    def get_button_text_in_first_card(self) -> str:
        """
        Возвращает текст кнопки в первой карточке.

        Returns:
            str: текст кнопки (например, "Купить" или "Оформить")
        """
        first_card = WebDriverWait(
            self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.PRODUCT_CARD)
        )

        # Пытаемся найти кнопку "Оформить" (если она есть)
        try:
            button = first_card.find_element(*self.CHECKOUT_BUTTON_TEXT)
            return button.text.strip()
        except Exception:
            # Если нет "Оформить", ищем "Купить"
            try:
                button = first_card.find_element(*self.BUY_BUTTON)
                return button.text.strip()
            except Exception:
                return "Кнопка не найдена"

    @allure.step("Получить количество товаров в корзине")
    def sum_book_to_cart(self) -> int:
        """
        Возвращает количество книг в корзине.
        Если элемент корзины отсутствует в DOM - возвращает 0 (корзина пуста).
        Если элемент есть - возвращает число из него.
        """
        try:
            # Пытаемся найти элемент с таймаутом (например, 3 секунды)
            cart_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.CART_INDICATOR)
            )
            # Если элемент найден - берем его текст и преобразуем в число
            count = int(cart_element.text)
            return count
        except TimeoutException:
            # Элемента нет в DOM - корзина пуста
            return 0

    @allure.step("Прокрутить до элемента: {locator}")
    def scroll_to_element(self, locator: tuple, max_scrolls: int = 20) -> None:
        """
            Прокручивает страницу до появления элемента.
                locator: локатор элемента
                max_scrolls: максимальное количество прокруток
            Returns:
                WebElement: найденный элемент
            """
        for i in range(max_scrolls):
            try:
                element = self.driver.find_element(*locator)
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", element)
                time.sleep(0.3)
                return element
            except NoSuchElementException:
                self.driver.execute_script("window.scrollBy(0, 400);")
                raise NoSuchElementException(
                        f"❌ Элемент {locator} "
                        f"не найден после {max_scrolls} прокруток")
        return None
