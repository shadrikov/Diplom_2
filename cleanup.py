import requests
import allure
from api_client import ApiClient

class CleanUp:

    @staticmethod
    # Функция удаления пользователя 
    def delete_user(access_token):
        response = ApiClient.request_delete_user(access_token)
        if response.status_code != 202:
            allure.attach(
                body=response.text,
                name=f"Не удалось удалить пользователя: статус {response.status_code}",
                attachment_type=allure.attachment_type.TEXT
            )
            