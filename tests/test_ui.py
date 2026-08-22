import pytest
import allure
from pages.catalog_page import CatalogPage
from pages.cart_page import CardPage
from data.search_queries import SearchQueries


@pytest.mark.ui
@allure.title("Поиск по автору")
@allure.story("Поиск через поисковую стоку")
@pytest.mark.parametrize("query", SearchQueries.AUTHOR)
def test_search_author_positive(browser, query):
    catalog_page = CatalogPage(browser)
    catalog_page.open_catalog_page()
    catalog_page.enter_query(query)
    catalog_page.search()
    url = catalog_page.get_current_url()
    assert "search?phrase=" in url, "Страница поиска не загрузилась"
    authors = catalog_page.get_authors_from_books()
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
    catalog_page.open_catalog_page()
    catalog_page.enter_query(query)
    catalog_page.search()
    url = catalog_page.get_current_url()
    assert "search?phrase=" in url, "Страница поиска не загрузилась"
    titles = catalog_page.get_titles_from_books()
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
    catalog_page.open_catalog_page()
    before_books = catalog_page.sum_book_to_cart()
    catalog_page.add_first_book_to_cart()
    button_text = catalog_page.get_button_text_in_first_card()
    assert button_text == "Оформить", \
        f"Ожидался текст 'Оформить', получен '{button_text}'"
    print(" Книга добавлена в корзину, текст кнопки изменился")
    after_books = catalog_page.sum_book_to_cart()
    assert after_books == before_books + 1


@pytest.mark.ui
@allure.title("Удаление из корзины всех книг")
@allure.story("Удаление из корзины")
def test_delete_from_cart(browser):
    catalog_page = CatalogPage(browser)
    cart_page = CardPage(browser)
    catalog_page.open_catalog_page()
    button_text = catalog_page.get_button_text_in_first_card()
    if button_text == "Оформить":
        print("Книга уже в корзине, пропускаю добавление")
    else:
        print("3. Добавляю первую книгу в корзину")
        catalog_page.add_first_book_to_cart()
    button_text = catalog_page.get_button_text_in_first_card()
    assert button_text == "Оформить", \
        f"Ожидался текст 'Оформить', получен '{button_text}'"
    print("Книга добавлена в корзину, текст кнопки изменился")
    books = catalog_page.sum_book_to_cart()
    assert books > 0, "В корзине нет книг"
    catalog_page.go_to_cart()
    url = catalog_page.get_current_url()
    assert "cart" in url, "Страница корзины не загрузилась"
    cart_page.clear_cart()
    books = catalog_page.sum_book_to_cart()
    assert books == 0


@pytest.mark.ui
@allure.title("Переход в карточку товара")
def test_view_card(browser):
    catalog_page = CatalogPage(browser)
    catalog_page.open_catalog_page()
    catalog_page.view_card()
    url = catalog_page.get_current_url()
    assert "/product/" in url, "Карточка товара не загрузилась"
