# Можете сделать рандомный тестовый файл для проверки работы фикстуры
from utils.data_generator import DataGenerator

def test_db_requests(super_admin, db_helper, created_test_user):
    assert created_test_user == db_helper.get_user_id(created_test_user.id)
    assert db_helper.user_exists_by_email("api1@gmail.com")

def test_db_movie(super_admin, db_helper, created_movie_db):
    movie_date = DataGenerator.generate_movie_data()
    movie_name = movie_date["name"]

    assert db_helper.get_movie_by_name(movie_name) is None
    created_mov = super_admin.api.movies_api.create_movie(movie_date)
    movie_id = created_mov.json()['id']
    assert db_helper.get_movie_by_name(movie_name) is not None
    super_admin.api.movies_api.delete_movie(movie_id=movie_id)
    assert db_helper.get_movie_by_name(movie_name) is None
