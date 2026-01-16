import requests


from clients.api_manager import ApiManager


class TestMovies:
    def test_create_movie(self, api_manager: ApiManager, movie_data):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.create_movie(movie_data=movie_data)
        assert response.status_code == 201, "Ошибка создании фильма"
        response_data = response.json()
        assert response_data["name"] == movie_data["name"]
        assert response_data["price"] == movie_data["price"]
        assert response_data["description"] == movie_data["description"]
        assert response_data["location"] == movie_data["location"]
        assert response_data["imageUrl"] == movie_data["imageUrl"]
        assert response_data["genreId"] == movie_data["genreId"]
        assert "id" in response_data
        assert "published" in response_data
        assert "rating" in response_data
        assert "createdAt" in response_data
        assert "genre" in response_data

    def test_create_movie_missing_required_fields(self, api_manager: ApiManager, movie_data):
        api_manager.auth_api.authenticate()
        required_fields = ["name", "price", "genreId", "location", "genreId"]
        for field in required_fields:
            invalid_data = movie_data.copy()
            del invalid_data[field]
            response = api_manager.movies_api.create_movie(
                movie_data=invalid_data,
                expected_status=400
            )
            assert response.status_code == 400, "Поле не обязательное"
            response_data = response.json()
            assert field not in response_data, "Поле не было удалено"

    def test_create_movie_invalid_value(self, api_manager: ApiManager, movie_data):
        api_manager.auth_api.authenticate()
        test_cases = [
            {"name": 123},
            {"imageUrl": 123},
            {"imageUrl": "htttttps"},
            {"price": "123"},
            {"description": 123},
            {"location": "TVR"},
            {"location": 123},
            {"published": 123},
            {"published": "123"},
            {"genreId": "test"},
            {"genreId": 123}

        ]
        for invalid_field in test_cases:
            test_data = movie_data.copy()
            test_data.update(invalid_field)
            response = api_manager.movies_api.create_movie(
                movie_data=test_data,
                expected_status=400
            )

            assert response.status_code == 400







