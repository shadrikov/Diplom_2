import pytest
import requests
from data import *
import allure
from api_client import ApiClient

class TestCreateOrder:

    @allure.title('Успешное создание заказа авторизованным пользователем')
    def test_create_order_with_authorized_user(self, user_data, create_new_user, ingredients_hash):
        response_registration = create_new_user(user_data)
        access_token = response_registration.json()['accessToken']
        payload = {
            'ingredients': ingredients_hash
            }
        response = ApiClient.post_request_create_order(payload, access_token)
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert Flags.ORDER_NAME in response.json()
        assert Flags.ORDER_NUMBER in response.json()[Flags.ORDER_DATA]

    @allure.title('Успешное создание заказа неавторизованным пользователем')
    # Уточнил серую зону: наставники отвечают, что ответ должен быть в статусе 200 ОК
    def test_create_order_with_unauthorized_user(self, ingredients_hash):
        payload = {
            'ingredients': ingredients_hash
            }
        response = ApiClient.post_request_create_order(payload)
        assert response.status_code == 200
        assert response.json()['success'] == True
        assert Flags.ORDER_NAME in response.json()
        assert Flags.ORDER_NUMBER in response.json()[Flags.ORDER_DATA]      

    @allure.title('Невозможность создания заказа без ингредиентов (400 Bad Request)')
    def test_create_order_without_ingredients_error(self, user_data, create_new_user):
        response_registration = create_new_user(user_data)
        access_token = response_registration.json()['accessToken']
        payload = {}
        response = ApiClient.post_request_create_order(payload, access_token)
        assert response.status_code == 400
        assert response.json()['success'] == False
        assert response.json()['message'] == ResponseMessages.CREATE_ORDER_WITHOUT_INGREDIENTS

    @allure.title('Невозможность создания заказа c неверным хешем ингредиента')
    def test_create_order_with_incorrect_ingredient_hash_error(self, user_data, create_new_user):
        response_registration = create_new_user(user_data)
        access_token = response_registration.json()['accessToken']
        payload = {
            'ingredients': ['60d3b41abdacab0026a733c6']
        }
        response = ApiClient.post_request_create_order(payload, access_token)
        assert response.status_code == 400
        assert response.json()['success'] == False
        assert response.json()['message'] == ResponseMessages.CREATE_ORDER_WITH_INCORRECT_INGREDIENT_HASH