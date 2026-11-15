import pytest
import generators
import requests
import allure
from cleanup import CleanUp
from api_client import ApiClient

# Фикстура генерации данных нового пользователя
@pytest.fixture
def user_data():
    user_data = {
        'email': generators.user_email_generator(),
        'password': 'password',
        'name': generators.user_name_generator()
    }
    return user_data

# Фикстура-фабрика создания нового пользователя и удаления его после теста
@pytest.fixture
def create_new_user():
    user_tokens = []

    def _create(payload):
        # отправляем запрос на регистрацию пользователя и сохраняем ответ в переменную response
        response = ApiClient.post_request_create_user(payload)

        if response.status_code != 200:
            allure.attach(
                body=response.text,
                name=f"Не удалось зарегистрировать пользователя: статус {response.status_code}",
                attachment_type=allure.attachment_type.TEXT
            )

        # получаем accessToken пользователя и добавляем его в список
        access_token = response.json()['accessToken']
        if access_token:
            user_tokens.append(access_token)
        
        # возвращаем в тест ответ на запрос создания пользователя
        return response

    # передаём функцию создания пользователя в тест
    yield _create 

    # удаляем пользователей после теста
    for access_token in user_tokens:
        CleanUp.delete_user(access_token)      

# Фикстура удаления пользователя после теста
@pytest.fixture
def cleanup_user():
    user_tokens = []

    # получаем accessToken пользователя и сохраняем его
    def get_access_token(access_token):
        if access_token:
            user_tokens.append(access_token)

    # передаём функцию получения accessToken в тест
    yield get_access_token 

    # удаляем пользователей после теста
    for access_token in user_tokens:
        CleanUp.delete_user(access_token)      

# Фикстура получения хеша двух ингредиентов
@pytest.fixture
def ingredients_hash():
    response = ApiClient.get_request_get_ingredients()
    ingredients_hash = [(response.json()['data'][0]['_id']), (response.json()['data'][1]['_id'])]
    return ingredients_hash
