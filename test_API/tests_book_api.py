import requests
import pytest
import allure
from config import base_url, HEADERS


@pytest.mark.api
@allure.title("Получить список книг в корзине")
@allure.story("Просмотр корзины")
def test_get_books():

    cart_url = f"{base_url}/v1/cart"
    resp = requests.get(cart_url, headers=HEADERS)
    assert resp.status_code == 200, f"Ошибка: {resp.status_code}"
    cart = resp.json()["products"]
    print(cart)


@pytest.mark.api
@allure.title("Добавление книги в корзину")
@allure.story("Добавление в корзину")
def test_add_book():
    """Тест добавления товара в корзину"""
    # Данные
    url = f"{base_url}/v1/cart/product"
    product_id = 2995498

    response = requests.post(url, headers=HEADERS, json={"id": product_id})
    assert response.status_code == 200, "Ошибка запроса"


@pytest.mark.api
@allure.title("Удалить все книги из корзины")
@allure.story("Удаление из корзины")
def test_delete_all():
    cart_url = f"{base_url}/v1/cart"
    response = requests.delete(
        cart_url, headers=HEADERS, json={"deleteAll": True})
    assert response.status_code == 204, "Ошибка очистки"


@pytest.mark.api
@allure.title("Добавление в корзину книги с несуществующим id")
@allure.story("Добавление в корзину")
def test_add_error_id():
    # Данные
    url = f"{base_url}/v1/cart/product"
    product_id = 2995498867

    response = requests.post(url, headers=HEADERS, json={"id": product_id})
    assert response.status_code == 400


@pytest.mark.api
@allure.title("Добавление книги в корзину без авторизации")
@allure.story("Добавление в корзину")
def test_add_not_authorized():
    url = f"{base_url}/v1/cart/product"
    product_id = 2995498
    response = requests.post(url, json={"id": product_id})
    assert response.status_code == 401
