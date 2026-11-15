import pytest
import requests
from data import *
import allure
from api_client import ApiClient

class TestCreateUser:

    @allure.title('Успешное создание уникального пользователя')
    def test_create_unique_user_success(self, user_data, cleanup_user):
        response = ApiClient.post_request_create_user(user_data)
        # Получение токена пользователя для последующего удаления
        cleanup_user(response.json()['accessToken'])
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert Flags.USER_DATA in response.json()
        assert Flags.ACCESS_TOKEN in response.json()
        assert Flags.REFRESH_TOKEN in response.json()

    @allure.title('Невозможность создания пользователя, который уже зарегистрирован')
    def test_create_user_repeating_email_error(self, user_data, create_new_user):   
        create_new_user(user_data)
        response = ApiClient.post_request_create_user(user_data)
        assert response.status_code == 403
        assert response.json()['success'] == False
        assert response.json()['message'] == ResponseMessages.CREATE_USER_WITH_REPEATING_EMAIL

    @allure.title('Невозможность создания пользователя без заполнения обязательных полей')
    @pytest.mark.parametrize('key',['email', 'password', 'name'])
    def test_create_user_missing_required_fields_error(self, key, user_data):
        # Копируем данные в новую переменную
        incomplete_data = user_data.copy()
        # Удаляем из словаря один из обязательных ключей
        del incomplete_data[key]
        response = ApiClient.post_request_create_user(incomplete_data)
        assert response.status_code == 403
        assert response.json()['success'] == False
        assert response.json()['message'] == ResponseMessages.CREATE_USER_MISSING_REQUIRED_FIELDS

class TestLoginUser:

    @allure.title('Успешный вход под существующим пользователем')
    def test_login_user_success(self, user_data, create_new_user):
        create_new_user(user_data)
        payload = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response = ApiClient.post_request_login_user(payload)
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert Flags.USER_DATA in response.json()
        assert Flags.ACCESS_TOKEN in response.json()
        assert Flags.REFRESH_TOKEN in response.json()

    @allure.title('Невозможность авторизации пользователя с некорректной парой логин/пароль')
    @pytest.mark.parametrize('key',['email', 'password'])
    def test_login_user_incorrect_credentials_error(self, key, user_data, create_new_user):
        create_new_user(user_data)
        payload = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        payload[key] = 'incorrect_data'
        response = ApiClient.post_request_login_user(payload)
        assert response.status_code == 401
        assert response.json()['success'] == False
        assert response.json()['message'] == ResponseMessages.LOGIN_USER_WITH_INCORRECT_LOGPASSW
    