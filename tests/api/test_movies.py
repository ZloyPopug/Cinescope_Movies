import pytest
from conftest import super_admin, common_user, admin_user
from utils.data_generator import DataGenerator
import allure
from models.movies_model import MovieResponse, BaseMovie


@allure.epic("Тестирование Фильмов")
class TestMovies:
    @allure.story("Тестирование создания фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie(self, super_admin, movie_data: BaseMovie):
        with allure.step("Создаем фильм под ролью Супер админа"):
            response = super_admin.api.movies_api.create_movie(movie_data=movie_data)
            response_movie = MovieResponse(**response.json())
        with allure.step("Сравниваем поля фильма с исходными данными"):
            assert response_movie.name == movie_data.name
            assert response_movie.price == movie_data.price
            assert response_movie.description == movie_data.description
            assert response_movie.location == movie_data.location
            assert response_movie.imageUrl == movie_data.imageUrl
            assert response_movie.genreId == movie_data.genreId
        with allure.step("Проверяем есть ли поля в созданном фильме"):
            assert response_movie.id is not None
            assert response_movie.published is not None
            assert response_movie.createdAt is not None
            assert response_movie.genre.name is not None

    @allure.story("Попытка создания фильма под Ролью Юзер")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.slow
    def test_create_movie_user(self, common_user, movie_data: BaseMovie):
        with allure.step("Пытаемся создать фильм под ролью Юзер"):
            common_user.api.movies_api.create_movie(movie_data=movie_data, expected_status=403)

    @allure.story("Попытка создания фильма под Ролью Админа")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.slow
    def test_create_movie_admin(self, admin_user, movie_data: BaseMovie):
        with allure.step("Пытаемся создать фильм под ролью Админа"):
            admin_user.api.movies_api.create_movie(movie_data=movie_data, expected_status=403)

    @allure.story("Попытка создания фильма с теми же тестовыми данными")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_already_exists(self, created_movie, super_admin, movie_data: BaseMovie):
        with allure.step("Пытаемся создать фильм с тем же тестовыми данными"):
            super_admin.api.movies_api.create_movie(movie_data=movie_data, expected_status=409)

    @allure.story("Попытка создания фильма без поля name")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_missing_required_field_name(self, super_admin, movie_data: BaseMovie):
        with allure.step("Делаем копию тестовых данных и удаляем поле name"):
            invalid_data = movie_data.model_dump()
            del invalid_data["name"]
        with allure.step("Пытаемся создать фильм без поля name"):
            response = super_admin.api.movies_api.create_movie(movie_data=invalid_data,expected_status=400)
        response_data = response.json()
        with allure.step("Проверяем, что статус ошибки корректный и содержится поле 'error'"):
            assert response_data["statusCode"] == 400, "Статус ответа не 400"
            assert response_data["error"] == "Bad Request", "Ошибка должна быть 'Bad Request'"

    @allure.story("Попытка создания фильма с неккоректным полем name")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_invalid_values(self, super_admin, movie_data: BaseMovie):
        with allure.step("Делаем копию тестовых данных и меняем поле name"):
            invalid_data = movie_data.model_dump()
            invalid_data["name"] = 123
        with allure.step("Пытаемся создать фильм с неккоректным полем name"):
            response = super_admin.api.movies_api.create_movie(movie_data=invalid_data,expected_status=400)
        response_data = response.json()
        with allure.step("Проверяем, что статус ошибки корректный и содержится поле 'error'"):
            assert response_data["statusCode"] == 400, "Статус ответа не 400"
            assert response_data["error"] == "Bad Request", "Ошибка должна быть 'Bad Request'"

    @allure.story("Получение фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movie(self, created_movie, super_admin):
        movie_id = created_movie.id
        with allure.step("Получаем фильм по id"):
            super_admin.api.movies_api.get_movie(movie_id=movie_id)

    @allure.story("Попытка получение фильма по неккоректному id")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.slow
    def test_get_movie_invalid_id(self, common_user):
        with allure.step("Пытаемся получить фильм по неккоректному id"):
            common_user.api.movies_api.get_movie(movie_id=-1, expected_status=404)

    @allure.story("Тестирование удаления фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_movie(self, created_movie, super_admin):
        movie_id = created_movie.id
        with allure.step("Удаляем фильм по id"):
            super_admin.api.movies_api.delete_movie(movie_id=movie_id)

    @allure.story("Тестирование удаления фильма по невалидному id")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_movie_invalid_id(self, super_admin):
        with allure.step("Пытаемся удалить фильм по неккортному id"):
            super_admin.api.movies_api.delete_movie(movie_id=-1, expected_status=404)

    @allure.story("Тестирование Обновления фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_movie(self, created_movie, super_admin):
        with allure.step("Записываем id созданного фильма в переменную"):
            movie_id = created_movie.id
        with allure.step("Создаем переменную с данными созданного фильма"):
            original_data = created_movie.copy()
        with allure.step("Генерируем новые данные для создания фильма"):
            new_data = DataGenerator.generate_movie_data(exclude_genre_id=original_data.genreId)
        with allure.step("Проверяем что данные не одинаковые"):
            assert new_data.name != original_data.name, "Сгенерировались одинаковые данные"
        with allure.step("Обновляем фильм с новыми данными по id"):
            response = super_admin.api.movies_api.update_movie(movie_id=movie_id, movie_data=new_data)
        update_data = MovieResponse(**response.json())
        with allure.step("Сравниваем поля фильма с исходными данными, проверяя что они не одинаковы"):
            assert new_data.name == update_data.name
            assert update_data.name != original_data.name
            assert update_data.price != original_data.price
            assert update_data.description != original_data.description
            assert update_data.imageUrl != original_data.imageUrl
            assert update_data.genreId != original_data.genreId

    @allure.story("Тестирование Обновления фильма с невалидным полем")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_movie_invalid_value(self, created_movie, super_admin):
        with allure.step("Записываем id созданного фильма в переменную"):
            movie_id = created_movie.id
        with allure.step("Создаем переменную с данными созданного фильма"):
            original_data = created_movie.copy()
        with allure.step("Генерируем новые данные для создания фильма"):
            new_data = DataGenerator.generate_movie_data()
        with allure.step("Проверяем что данные не одинаковые"):
            assert new_data.name != original_data.name, "Сгенерировались одинаковые данные"
        with allure.step("Меняем поле name на неваилидное значение"):
            new_data.name = 123
        with allure.step("Пытаемся обновить фильм с невалидными данными"):
           response = super_admin.api.movies_api.update_movie(movie_id=movie_id, movie_data=new_data, expected_status=400)
        response_data = response.json()
        with allure.step("Проверяем, что статус ошибки корректный и содержится поле 'error'"):
            assert response_data["statusCode"] == 400, "Статус ответа не 400"
            assert response_data["error"] == "Bad Request", "Ошибка должна быть 'Bad Request'"
        with allure.step("Проверяем, что сообщение об ошибке содержит текст про 'name'"):
            expected_text = "Поле name должно быть строкой"
            messages = response_data.get("message", [])
            assert any(expected_text in msg for msg in messages), \
                f"Ожидаемое сообщение '{expected_text}' не найдено в {messages}"

    @allure.story("Тестирование Обновления фильма с невалидным id")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_movie_invalid_id(self, created_movie, super_admin):
        with allure.step("Создаем переменную с данными созданного фильма"):
            original_data = created_movie.copy()
        with allure.step("Генерируем новые данные для создания фильма"):
            new_data = DataGenerator.generate_movie_data()
        with allure.step("Проверяем что данные не одинаковые"):
            assert new_data.name != original_data.name, "Сгенерировались одинаковые данные"
        with allure.step("Пытаемся обновить фильм с невалидным id"):
            response = super_admin.api.movies_api.update_movie(movie_data=new_data, movie_id=-1, expected_status=404)
        response_data = response.json()
        with allure.step("Проверяем текст сообщения об ошибке"):
            expected_message = "Фильм не найден"
            assert response_data["message"] == expected_message, \
                f"Ожидаемое сообщение '{expected_message}' не совпадает с фактическим '{response_data['message']}'"

    @allure.story("Тестирование Фильтрации по рандомным параметрам")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movies_with_filters(self,  super_admin):
        with allure.step("Генерируем рандомные значения для фильтрации"):
            params = DataGenerator.generate_movie_filter_params()
        with allure.step("Отправляем запрос для получения фильмов по параметрам"):
            super_admin.api.movies_api.get_movies_with_filters(params=params)

    @allure.story("Тестирование Фильтрации по полю locations")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movies_with_location_filter(self,  super_admin):
        with allure.step("Создаем переменнную с полем локация"):
            params = {
                "locations": ["MSK"]
            }
        with allure.step("Отправляем запрос для получения фильмов по локации"):
            response = super_admin.api.movies_api.get_movies_with_filters(params)
        with allure.step("Проверяем что в полученном списке фильмов только искомые фильмы"):
            movies = response.json()["movies"]
            for movie in movies:
                assert movie["location"] == "MSK"

    @allure.story("Тестирование Фильтрации по полю price")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movies_with_price_filter(self,  super_admin):
        with allure.step("Создаем переменнную с полями minPrice и maxPrice"):
            params = {
                "minPrice": 500,
                "maxPrice": 800
            }
        with allure.step("Отправляем запрос для получения фильмов по price"):
            response = super_admin.api.movies_api.get_movies_with_filters(params)
        with allure.step("Проверяем что в полученном списке фильмов только искомые фильмы"):
            movies = response.json()["movies"]
            for movie in movies:
                assert movie["price"] > 500
                assert movie["price"] < 800

    @allure.story("Тестирование Фильтрации по полю price с невалидными данными")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movies_invalid_price_type(self,  super_admin):
        with allure.step("Создаем переменнную с полями minPrice и maxPrice"):
            params = {
                "minPrice": "Строка",
                "maxPrice": "Строка"
            }
        with allure.step("Пытаемся получить фильмы по невалидным данным"):
            super_admin.api.movies_api.get_movies_with_filters(params=params, expected_status=400)

    @allure.story("Тестирование Фильтрации с параметизацией")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.parametrize("minPrice,maxPrice,locations,genreId", [(100, 400, "MSK", 2), (200, 800, "SPB", 1)], ids=['MSK', "SPB"])
    def test_get_params(self, super_admin, minPrice, maxPrice, locations, genreId):
        with allure.step("Создаем переменнную с полями для фильтрации"):
            params = {
                "minPrice": minPrice,
                "maxPrice": maxPrice,
                "locations": locations,
                "genreId": genreId
            }
        with allure.step("Отправляем запрос для получении фильмов по параметрам"):
            response = super_admin.api.movies_api.get_movies_with_filters(params=params)
        with allure.step("Проверяем что в полученном списке фильмов только искомые фильмы"):
            movies = response.json()["movies"]
            for movie in movies:
                assert movie["price"] > minPrice
                assert movie["price"] < maxPrice
                assert movie["location"] == locations
                assert movie["genreId"] == genreId

    @allure.story("Тестирование ролевой модели с параметизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.slow
    @pytest.mark.parametrize("fixture_name,expected_status",[("super_admin", 200), ("common_user", 403), ("admin_user", 403)])
    def test_delete_movie_roles(self, request, created_movie, fixture_name,expected_status):
        with allure.step("Записывем id созданного фильма в переменную"):
            movie_id = created_movie.id
        user = request.getfixturevalue(fixture_name)
        with allure.step("Пытаемся удалить фильм"):
            user.api.movies_api.delete_movie(movie_id=movie_id, expected_status=expected_status)

    @allure.story("Создание фильма с проверкой в БД")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.db
    def test_db_movie(self, super_admin, db_helper, created_movie_db):
        with allure.step("Генерируем тестовые данные для фильма"):
            movie_date = DataGenerator.generate_movie_data()
            movie_name = movie_date.name
        with allure.step("Проверяем, что фильма нет в БД до создания"):
            assert db_helper.get_movie_by_name(movie_name) is None
        with allure.step("Создаем фильм через API"):
            created_mov = super_admin.api.movies_api.create_movie(movie_date)
            movie_id = created_mov.json()['id']
        with allure.step("Проверяем, что фильм появился в БД"):
            assert db_helper.get_movie_by_name(movie_name) is not None
        with allure.step("Удаляем фильм через API"):
            super_admin.api.movies_api.delete_movie(movie_id=movie_id)
        with allure.step("Проверяем, что фильм удален из БД"):
            assert db_helper.get_movie_by_name(movie_name) is None

