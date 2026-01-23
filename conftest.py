from clients.api_manager import ApiManager
import requests
from constans import BASE_URL
import pytest
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session():

    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="function")
def movie_data():
    random_name = DataGenerator.generate_random_movie_name()
    random_imageUrl = DataGenerator.generate_random_image_url()
    random_price = DataGenerator.generate_random_price()
    random_description = DataGenerator.generate_random_description()
    random_location = DataGenerator.generate_random_location()
    random_published = DataGenerator.generate_random_published()
    random_genreId = DataGenerator.generate_random_genreId()

    return {
        "name": random_name,
        "imageUrl": random_imageUrl,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": random_genreId
    }

@pytest.fixture(scope="function")
def created_movie(api_manager: ApiManager,movie_data):
    api_manager.auth_api.authenticate()
    response = api_manager.movies_api.create_movie(movie_data)
    assert response.status_code == 201
    movie_info = response.json()
    movie_id = movie_info["id"]

    yield movie_info
    try:
        api_manager.movies_api.delete_movie(movie_id, expected_status=200)
    except ValueError as e:
        if "Expected: 200" in str(e):
            print(f"Фильм {movie_id} уже удален или не найден")
        else:
            raise

@pytest.fixture(scope="function")
def reviews_data():
    reviews_data = DataGenerator.generate_reviews_data()
    return reviews_data

@pytest.fixture(scope="function")
def created_reviews(created_movie, reviews_data, api_manager: ApiManager):
    api_manager.auth_api.authenticate()
    movie_id = created_movie["id"]
    api_manager.movies_api.create_reviews(movie_id=movie_id, reviews_data=reviews_data)
    return movie_id

@pytest.fixture(scope="session")
def auth_session(api_manager):
    response = api_manager.auth_api.authenticate()
    user_Id = response["user"]["id"]
    return user_Id




