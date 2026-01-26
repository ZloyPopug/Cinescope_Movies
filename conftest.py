from clients.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from entities.user import User
import requests
from constans import BASE_URL
import pytest
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from constants.roles import Roles


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
def created_movie(super_admin, movie_data):
    response = super_admin.api.movies_api.create_movie(movie_data)
    assert response.status_code == 201
    movie_info = response.json()
    movie_id = movie_info["id"]

    yield movie_info
    try:
        super_admin.api.movies_api.delete_movie(movie_id, expected_status=200)
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
def created_reviews(super_admin, created_movie, reviews_data):
    movie_id = created_movie["id"]
    super_admin.api.reviews_api.create_reviews(movie_id=movie_id, reviews_data=reviews_data)
    return movie_id

@pytest.fixture(scope="session")
def auth_session(api_manager):
    response = api_manager.auth_api.authenticate(
        (SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD)
    )
    user_Id = response["user"]["id"]
    return user_Id

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_fullname = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_fullname,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session)

    create_response = super_admin.api.user_api.create_user(creation_user_data)
    user_id = create_response.json()["id"]
    super_admin.api.user_api.update_user(user_data={
        "roles": [Roles.ADMIN.value]
    }, user_locator=user_id)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user
