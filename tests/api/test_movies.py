import requests

from conftest import api_manager
from constans import BASE_URL,HEADERS,LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from clients.api_manager import ApiManager


class TestMovies:
    def test_create_movies(self, api_manager: ApiManager, ):
        response = api_manager.auth_api.authenticate
        assert response.status_code == 200, "Ошибка при регистрации"
        response_data = response.json()



