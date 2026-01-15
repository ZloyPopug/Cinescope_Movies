import requests


from clients.api_manager import ApiManager


class TestMovies:
    def test_create_movies(self, api_manager: ApiManager, movie_data):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.create_movie(movie_data=movie_data)
        assert response.status_code == 201, "Ошибка создании фильма"




