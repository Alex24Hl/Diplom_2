import allure
import requests
import sys

from url import BASE_URL
from data import Data
from conftest import auth_token, get_ingredients

sys.path.insert(1, "../pages")

class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized_with_ingredients(self, auth_token, get_ingredients):
        headers = {"Authorization": auth_token}
        ingredients = [ingredient["_id"] for ingredient in get_ingredients[:2]]
        payload = {"ingredients": ingredients}
        response = requests.post(f"{BASE_URL}/orders", headers=headers, json=payload)
        assert response.status_code == 200
        assert "name" in response.json()

    @allure.title('Тест на cоздание заказа без авторизации, но с ингредиентами')
    def test_create_order_unauthorized_with_ingredients_success(self, get_ingredients):
        ingredients = [ingredient["_id"] for ingredient in get_ingredients[:2]]
        payload = {"ingredients": ingredients}
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 200
        assert "order" in response.json()

    @allure.title('Тест на cоздание заказа с авторизацией, но без ингредиентов')
    def test_create_order_authorized_without_ingredients(self, auth_token):
        headers = {"Authorization": auth_token}
        payload = {"ingredients": []}
        response = requests.post(f"{BASE_URL}/orders", headers=headers, json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == Data.NEED_INGREDIENTS

    @allure.title("Тест на создание заказа без авторизации и без ингредиентов")
    def test_create_order_unauthorized_without_ingredients(self):
        payload = {"ingredients": []}
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == Data.NEED_INGREDIENTS

    @allure.title("Тест на создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_hash_ingredients(self):
        payload = {"ingredients": ["invalid_hash_1", "invalid_hash_2"]}
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 500
