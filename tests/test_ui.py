import pytest
import allure
from pages.catalog_page import CatalogPage
from pages.cart_page import CardPage
from data.search_queries import SearchQueries


@pytest.mark.ui
@allure.title("Поиск по автору")
@allure.story("Поиск через поисковую стоку")
@pytest.mark.parametrize("query", SearchQueries.AUTHOR)
def test_search_author_positive(browser, query) -> list:
    catalog_page = CatalogPage(browser)
    with allure.step("Открыть страницу каталога"):
        catalog_page.open_catalog_page()
    with allure.step("Ввести запрос в строку поиска"):
        catalog_page.enter_query(query)
    with allure.step("Нажать кнопку поиска"):
        catalog_page.search()
    with allure.step("Получить текущий URL"):
        url = catalog_page.get_current_url()
    with allure.step("Проверить загрузку страницы поиска"):
        assert "search?phrase=" in url, "Страница поиска не загрузилась"
    with allure.step("Получить список авторов первых 5 книг"):
        authors = catalog_page.get_authors_from_books()
    with allure.step("Проверить соответствие результатов поиска запросу"):
        assert len(authors) > 0, " Результаты поиска не найдены!"
    for author in authors:
        assert query.lower() in author.lower(), \
            f"В имени '{author}' нет '{query}'"

    print(f" Все {len(authors)} книг содержат '{query}'")
    return authors


@pytest.mark.ui
@allure.title("Поиск по названию книги")
@allure.story("Поиск через поисковую стоку")
@pytest.mark.parametrize("query", SearchQueries.TITLE)
def test_search_title_positive(browser, query):
    catalog_page = CatalogPage(browser)
    with allure.step("Открыть страницу каталога"):
        catalog_page.open_catalog_page()
    with allure.step("Ввести запрос в строку поиска"):
        catalog_page.enter_query(query)
    with allure.step("Нажать кнопку поиска"):
        catalog_page.search()
    with allure.step("Получить текущий URL"):
        url = catalog_page.get_current_url()
    with allure.step("Проверить загрузку страницы поиска"):
        assert "search?phrase=" in url, "Страница поиска не загрузилась"
    with allure.step("Получить список названий первых 5 книг"):
        titles = catalog_page.get_titles_from_books()
    with allure.step("Проверить соответствие результатов поиска запросу"):
        assert len(titles) > 0, " Результаты поиска не найдены!"
    for title in titles:
        assert query.lower() in title.lower(), \
            f"В имени '{title}' нет '{query}'"

    print(f" Все {len(titles)} книг содержат '{query}'")
    return titles


@pytest.mark.ui
@allure.title("Добавление книги в корзину")
@allure.story("Добавление в корзину")
def test_add_to_cart(browser):
    catalog_page = CatalogPage(browser)
    with allure.step("Открыть страницу каталога"):
        catalog_page.open_catalog_page()
    with allure.step("Получить количество книг в корзине"):
        before_books = catalog_page.sum_book_to_cart()
    with allure.step("Нажать кнопку 'Купить' в карточке каталога"):
        catalog_page.add_first_book_to_cart()
    with allure.step("Получить текст кнопки после нажатия"):
        button_text = catalog_page.get_button_text_in_first_card()
    with (allure.step("Проверить, что текст кнопки изменился на 'Оформить'")):
        assert button_text == "Оформить", (f"Ожидался текст 'Оформить', "
                                           f"получен '{button_text}'")
    print(" Книга добавлена в корзину, текст кнопки изменился")
    with allure.step("Получить количество книг в корзине"):
        after_books = catalog_page.sum_book_to_cart()
    with allure.step("Проверить, что количество книг в корзине увеличилось"):
        assert after_books == before_books + 1


@pytest.mark.ui
@allure.title("Удаление из корзины всех книг")
@allure.story("Удаление из корзины")
def test_delete_from_cart(browser):
    catalog_page = CatalogPage(browser)
    cart_page = CardPage(browser)
    with allure.step("Открыть страницу каталога"):
        catalog_page.open_catalog_page()
    with allure.step("Добавить книгу в корзину"):
        button_text = catalog_page.get_button_text_in_first_card()
    if button_text == "Оформить":
        print("Книга уже в корзине, пропускаю добавление")
    else:
        print("3. Добавляю первую книгу в корзину")
        catalog_page.add_first_book_to_cart()
    button_text = catalog_page.get_button_text_in_first_card()
    with allure.step("Проверить, что текст кнопки изменился на 'Оформить'"):
        assert button_text == "Оформить", (f"Ожидался текст 'Оформить', "
                                           f"получен '{button_text}'")
    print("Книга добавлена в корзину, текст кнопки изменился")
    with allure.step("Получить количество книг в корзине"):
        books = catalog_page.sum_book_to_cart()
    with allure.step("Проверить количество книг в корзине"):
        assert books > 0, "В корзине нет книг"
    with allure.step("Перейти в корзину"):
        catalog_page.go_to_cart()
    with allure.step("Получить текущий URL"):
        url = catalog_page.get_current_url()
    with allure.step("Проверить, что корзина загрузилась"):
        assert "cart" in url, "Страница корзины не загрузилась"
    with allure.step("Нажать кнопку Очистить корзину"):
        cart_page.clear_cart()
    with allure.step("Получить количество книг в корзине"):
        books = catalog_page.sum_book_to_cart()
    with allure.step("Проверить, что корзина пуста"):
        assert books == 0


@pytest.mark.ui
@allure.title("Переход в карточку товара")
def test_view_card(browser):
    catalog_page = CatalogPage(browser)
    with allure.step("Открыть страницу каталога"):
        catalog_page.open_catalog_page()
    with allure.step("Перейти на страницу книги"):
        catalog_page.view_card()
    with allure.step("Получить текущий URL"):
        url = catalog_page.get_current_url()
    with allure.step("Проверить загрузку страницы книги"):
        assert "/product/" in url, "Карточка товара не загрузилась"
