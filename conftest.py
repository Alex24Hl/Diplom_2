import allure
import pytest
import requests
import string
import random

from url import BASE_URL

@allure.title('Фикстура генерации уникальных данных пользователя')
@pytest.fixture
def generate_unique_user():
    random_symbol = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        "email": f"user_{random_symbol}@yandex.com",
        "password": f"Password_{random_symbol}",
        "name": f"User_{random_symbol}"
    }

@allure.title('Фикстура регистрации пользователя')
@pytest.fixture
def register_user(generate_unique_user):
    user_data = generate_unique_user
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    return {
        "user_data": user_data,
        "response": response
    }

@allure.title('Фикстура получения токена авторизации')
@pytest.fixture
def auth_token(register_user):
    login_data = {
        "email": register_user["user_data"]["email"],
        "password": register_user["user_data"]["password"]
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    return response.json().get("accessToken")

@allure.title('Фикстура для генерации обновлённых уникальных значений')
@pytest.fixture(params=["email", "password", "name"])
def generate_field_value(request):
    field = request.param
    if field == "email":
        value = f"update_user_{random.randint(1000, 9999)}@test.com"
    elif field == "password":
        value = f"Password_{random.randint(1000, 9999)}"
    else:
        value = f"User_{random.randint(1000, 9999)}"
    return field, value

@allure.title('Фикстура получения ингредиентов')
@pytest.fixture
def get_ingredients():
    response = requests.get(f"{BASE_URL}/ingredients")
    return response.json()["data"]
