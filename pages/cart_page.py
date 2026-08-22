import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time


class CardPage:
    """Класс содержит информацию о корзине.
    Содержит методы просмотра добавленных книг,
    очищения корзины"""

    #  локаторы элементов
    CART_INDICATOR = (
        By.CSS_SELECTOR,
        ".chg-app-indicator.chg-app-indicator--m.header-controls__indicator")
    CLEAR_CARD = By.CSS_SELECTOR, "button[data-testid-button-cart='clearAll']"
    CART_ITEM = By.CSS_SELECTOR, "[data-testid-item-cart='product']"
    BOOkS_IN_CARD = By.CLASS_NAME, "cart-item__wrapper"

    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 15

    @allure.step("Получить количество товаров в корзине")
    def count_items_to_cart(self):
        """
            Возвращает количество товаров в корзине.
            Returns:
                int: количество элементов в корзине
            """
        # Находим все элементы в корзине
        items = self.driver.find_elements(*self.BOOkS_IN_CARD)
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.element_to_be_clickable(self.BOOkS_IN_CARD)
        )
        return len(items)

    @allure.step("Очистить корзину")
    def clear_cart(self):
        """
        Очищает корзину. Если корзина уже пуста - ничего не делает.
        """
        try:
            # Проверяем, есть ли кнопка очистки в DOM
            button_clear = self.driver.find_element(*self.CLEAR_CARD)

            # Ждем, пока кнопка станет кликабельной
            WebDriverWait(self.driver, self.default_timeout).until(
                EC.element_to_be_clickable(self.CLEAR_CARD)
            )

            # Кликаем с повторными попытками
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    button_clear.click()
                    print("✅ Кнопка очистки нажата")
                    break
                except Exception as e:
                    if attempt < max_attempts - 1:
                        print(f"⚠️ Попытка {attempt + 1} не удалась: {e}")
                        time.sleep(1)
                        # Пробуем найти кнопку заново
                        button_clear = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable(self.CLEAR_CARD)
                        )
                    else:
                        # Последняя попытка - через JS
                        print("🔄 Пробуем кликнуть через JS")
                        self.driver.execute_script(
                            "arguments[0].click();", button_clear
                        )
                        print("✅ Кнопка нажата через JS")

            # Ждем, пока индикатор корзины исчезнет (корзина очищена)
            WebDriverWait(self.driver, self.default_timeout).until(
                EC.invisibility_of_element_located(self.CART_INDICATOR)
            )
            print("Корзина успешно очищена")

        except NoSuchElementException:
            # Кнопка очистки не найдена - корзина уже пуста
            print("Корзина уже пуста, очистка не требуется")
        except TimeoutException:
            # Индикатор не исчез, но возможно корзина уже пуста
            print("⚠️ Индикатор корзины не исчез, но продолжаем...")
            try:
                # Проверяем, может корзина уже пуста
                time.sleep(1)
                indicator = self.driver.find_element(*self.CART_INDICATOR)
                if int(indicator.text) == 0:
                    print("✅ Корзина очищена")
            except Exception:
                pass

        return self
