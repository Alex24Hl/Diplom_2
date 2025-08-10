import allure
import requests
import sys

from conftest import register_user
from data import Data
from url import BASE_URL

sys.path.insert(1, "../pages")

class TestUserLogin:

    @allure.title('Тест на проверку логина под существующим пользователем')
    def test_login_existing_user_success(self, register_user):
        data = {
            "email": register_user["user_data"]["email"],
            "password": register_user["user_data"]["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        assert response.status_code == 200
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    @allure.title('Тест на проверку логина с неверным логином и паролем')
    def test_login_invalid_credentials_fail(self, register_user):
        data = {
            "email": register_user["user_data"]["email"],
            "password": "bad_password"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        assert response.status_code == 401
        assert response.json()["message"] == Data.INCORRECT_FIELDS
