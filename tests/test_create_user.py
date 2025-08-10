import allure
import pytest
import requests
import sys

from conftest import generate_unique_user, register_user
from data import Data
from url import BASE_URL

sys.path.insert(1, "../pages")

class TestCreateUser:

    @allure.title('Тест на проверку создания уникального пользователя')
    def test_create_unique_user_success(self, generate_unique_user):
        data = generate_unique_user
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        assert response.status_code == 200
        assert response.json()["user"]["email"] == data["email"]
        assert response.json()["user"]["name"] == data["name"]

    @allure.title('Тест на проверку создания дубликата пользователя')
    def test_create_duplicate_user(self, register_user):
        data = register_user["user_data"]
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        assert response.status_code == 403
        assert response.json()["message"] == Data.USER_ALREADY_EXISTS

    @allure.title('Тест на проверку создания пользователя без обязательного поля')
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_with_missing_field(self, generate_unique_user, field):
        data = generate_unique_user
        del data[field]
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        assert response.status_code == 403
        assert response.json()["message"] == Data.MISSING_REQUIRED_FIELDS
