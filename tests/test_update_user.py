import allure
import requests
import sys

from conftest import register_user, auth_token, generate_field_value
from url import BASE_URL
from data import Data

sys.path.insert(1, "../pages")


class TestUserUpdate:

    @allure.title('Тест на изменение данных у авторизованного пользователя')
    def test_update_user_authorized_success(self, auth_token, register_user, generate_field_value):
        field, new_value = generate_field_value
        data = register_user["user_data"]

        headers = {"Authorization": auth_token}

        update_data = {field: new_value}
        response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json=update_data)
        assert response.status_code == 200

        response_data = response.json()
        updated_user = response_data["user"]

        if field in ['email', 'name']:
            assert updated_user[field] == new_value
        elif field in ['password']:
            assert updated_user["email"] == data["email"]
            assert updated_user["name"] == data["name"]

    @allure.title('Тест на изменение данных у неавторизованного пользователя')
    def test_update_user_unauthorized_fail(self):
        response = requests.patch(
            f"{BASE_URL}/auth/user",
            json={"name": "UnauthorizedUser"}
        )
        assert response.status_code == 401
        assert response.json()["message"] == Data.AUTHORIZATION_REQUIRED