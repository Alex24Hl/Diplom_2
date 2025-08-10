import allure
import requests
import sys

from conftest import auth_token, get_ingredients
from url import BASE_URL
from data import Data

sys.path.insert(1, "../pages")


class TestGetUserOrders:

    @allure.title('Тест на получение заказов авторизованного пользователя')
    def test_get_user_orders_authorized_success(self, auth_token, get_ingredients):
        headers = {"Authorization": auth_token}
        ingredients = [ingredient["_id"] for ingredient in get_ingredients[:2]]
        requests.post(f"{BASE_URL}/orders", headers=headers, json={"ingredients": ingredients})
        response = requests.get(f"{BASE_URL}/orders", headers=headers)
        assert response.status_code == 200
        assert len(response.json()["orders"]) > 0

    @allure.title('Тест на получение заказов неавторизованным пользователем')
    def test_get_user_orders_unauthorized_fail(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 401
        assert response.json()["message"] == Data.AUTHORIZATION_REQUIRED