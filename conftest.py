from clients.api_manager import ApiManager
import requests
from constans import BASE_URL,HEADERS,LOGIN_ENDPOINT
import pytest
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator

@pytest.fixture(scope="session")
def requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():

    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="function")
def test_movie():
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

# {
#   "name": "Название фильма",
#   "imageUrl": "https://image.url",
#   "price": 100,
#   "description": "Описание фильма",
#   "location": "SPB",
#   "published": true,
#   "genreId": 1
# }'