from utils.data_generator import DataGenerator
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

    def test_create_movie_already_exists(self, created_movie, api_manager: ApiManager, movie_data):
        response = api_manager.movies_api.create_movie(movie_data=movie_data, expected_status=409)
        assert response.status_code == 409

    def test_create_movie_missing_required_field_name(self, api_manager:ApiManager, movie_data):
        api_manager.auth_api.authenticate()
        invalid_data = movie_data.copy()
        del invalid_data["name"]
        response = api_manager.movies_api.create_movie(movie_data=invalid_data,expected_status=400)
        assert response.status_code == 400
        response_data = response.json()
        assert "name" not in response_data, "Поле не было удалено"

    def test_create_movie_invalid_values(self, api_manager: ApiManager, movie_data):
        api_manager.auth_api.authenticate()
        invalid_data = movie_data.copy()
        invalid_data["name"] = 123
        response = api_manager.movies_api.create_movie(movie_data=invalid_data,expected_status=400)
        assert response.status_code == 400

    def test_get_movie(self, created_movie, api_manager: ApiManager):
        movie_id = created_movie["id"]
        response = api_manager.movies_api.get_movie(movie_id=movie_id)
        assert response.status_code == 200

    def test_get_movie_invalid_id(self, api_manager: ApiManager):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.get_movie(movie_id=-1, expected_status=404)
        assert response.status_code == 404

    def test_delete_movie(self, created_movie, api_manager:ApiManager):
        movie_id = created_movie["id"]
        response = api_manager.movies_api.delete_movie(movie_id=movie_id)
        assert response.status_code == 200

    def test_delete_movie_invalid_id(self, api_manager:ApiManager):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.delete_movie(movie_id=-1, expected_status=404)
        assert response.status_code == 404

    def test_update_movie(self, created_movie, api_manager:ApiManager):
        movie_id = created_movie["id"]
        original_data = created_movie.copy()
        new_data = DataGenerator.generate_movie_data(exclude_genre_id=original_data)
        assert new_data["name"] != original_data["name"], "Сгенерировались одинаковые данные"
        response = api_manager.movies_api.update_movie(movie_id=movie_id, movie_data=new_data)
        update_data = response.json()
        assert new_data["name"] == update_data["name"]
        assert update_data["name"] != original_data["name"]
        assert update_data["price"] != original_data["price"]
        assert update_data["description"] != original_data["description"]
        assert update_data["imageUrl"] != original_data["imageUrl"]
        assert update_data["genreId"] != original_data["genreId"]

    def test_update_movie_invalid_value(self, created_movie, api_manager:ApiManager):
        movie_id = created_movie["id"]
        original_data = created_movie.copy()
        new_data = DataGenerator.generate_movie_data()
        assert new_data["name"] != original_data["name"], "Сгенерировались одинаковые данные"
        new_data["name"] = 123
        response = api_manager.movies_api.update_movie(movie_id=movie_id, movie_data=new_data, expected_status=400)
        assert response.status_code == 400

    def test_update_movie_invalid_id(self, created_movie, api_manager:ApiManager):
        original_data = created_movie.copy()
        new_data = DataGenerator.generate_movie_data()
        assert new_data["name"] != original_data["name"], "Сгенерировались одинаковые данные"
        response = api_manager.movies_api.update_movie(movie_data=new_data, movie_id=-1, expected_status=404)
        assert response.status_code == 404

    def test_get_movies_with_filters(self, api_manager:ApiManager):
        api_manager.auth_api.authenticate()
        params = DataGenerator.generate_movie_filter_params()
        response = api_manager.movies_api.get_movies_with_filters(params=params)
        assert response.status_code == 200

    def test_get_movies_with_location_filter(self, api_manager:ApiManager):
        api_manager.auth_api.authenticate()
        params = {
            "locations": ["MSK"]
        }
        response = api_manager.movies_api.get_movies_with_filters(params)
        assert response.status_code == 200

    def test_get_movies_with_price_filter(self, api_manager:ApiManager):
        api_manager.auth_api.authenticate()
        params = {
            "minPrice": 500,
            "maxPrice": 800
        }
        response = api_manager.movies_api.get_movies_with_filters(params)
        assert response.status_code == 200

    def test_get_movies_invalid_price_type(self, api_manager:ApiManager):
        api_manager.auth_api.authenticate()
        params = {
            "minPrice": "Строка",
            "maxPrice": "Строка"
        }
        response = api_manager.movies_api.get_movies_with_filters(params=params, expected_status=400)
        assert response.status_code == 400

