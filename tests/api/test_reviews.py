import pytest
import allure

@allure.epic("Тестирование Отзывов")
class TestReviews:
    @allure.story("Тестирование создания отзыва")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_reviews(self, created_movie, reviews_data, super_admin):
        with allure.step("Записываем id созданного фильма в переменную"):
            movie_id = created_movie.id
        with allure.step("Создаем отзыв"):
            response = super_admin.api.reviews_api.create_reviews(movie_id=movie_id, reviews_data=reviews_data)
        response_data = response.json()
        with allure.step("Сравниваем поля отзыва с исходными данными"):
            assert response_data["text"] == reviews_data["text"]
            assert response_data["rating"] == reviews_data["rating"]

    @allure.story("Тестирование создания отзыва с невалидными данными")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_reviews_invalid_value(self, created_movie, super_admin):
        with allure.step("Записываем id созданного фильма в переменную"):
            movie_id = created_movie.id
        with allure.step("Создаем переменную с невалидными данными"):
            invalid_data = {
                "rating": "test",
                "text": 123
            }
        with allure.step("Пытаемся создать отзыв с невалидными данными"):
            super_admin.api.reviews_api.create_reviews(movie_id=movie_id, reviews_data=invalid_data, expected_status=400)

    @allure.story("Тестирование создания отзыва с несуществующим id фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_reviews_invalid_id(self, reviews_data, auth_session, super_admin):
        with allure.step("Записываем id несуществующего фильма в переменную"):
            movie_id = -1
        with allure.step("Пытаемся создать отзыв с невалидными данными"):
            super_admin.api.reviews_api.create_reviews(movie_id=movie_id,reviews_data=reviews_data,expected_status=404)

    @allure.story("Тестирование создания отзыва на фильм у которого уже есть отзыв")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_reviews_already_exists(self, created_reviews, reviews_data, super_admin):
        with allure.step("Записываем id фильма у которого уже есть отзыв в переменную"):
            movie_id = created_reviews
        with allure.step("Пытаемся создать отзыв на фильм с отзывом"):
            response = super_admin.api.reviews_api.create_reviews(movie_id=movie_id, reviews_data=reviews_data, expected_status=409)
        with allure.step("Проверяем текст сообщения об ошибке"):
            response_data = response.json()
            assert response_data["message"] == "Вы уже оставляли отзыв к этому фильму"

    @allure.story("Тестирование обновления отзыва на фильм")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_reviews(self,created_reviews, reviews_data, super_admin):
        with allure.step("Записываем id фильма с отзывом в переменную"):
            movie_id = created_reviews
        with allure.step("Обновляем отзыв у фильма"):
            response = super_admin.api.reviews_api.update_reviews(movie_id=movie_id, reviews_data=reviews_data)
        response_data = response.json()
        with allure.step("Сравниваем данные с исходными"):
            assert response_data["text"] == reviews_data["text"]
            assert response_data["rating"] == reviews_data["rating"]
            assert response_data["movieId"] == movie_id
        with allure.step("Проверяем что поля есть"):
            assert "userId" in response_data
            assert "hidden" in response_data
            assert "createdAt" in response_data

    @allure.story("Тестирование обновления отзыва на фильм с невалидными данными")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_reviews_invalid_value(self, created_reviews, super_admin):
        with allure.step("Записываем id фильма с отзывом в переменную"):
            movie_id = created_reviews
        with allure.step("Создаем переменную с невалидными данными"):
            invalid_data = {
                "rating": "test",
                "text": 123
            }
        with allure.step("Пытаемся обновить отзыв, с невалидными данными"):
            response = super_admin.api.reviews_api.update_reviews(movie_id=movie_id, reviews_data=invalid_data, expected_status=400)
        with allure.step("Проверяем текст сообщения об ошибке"):
            response_data = response.json()
            messages = response_data.get("message")
            assert "Поле rating должно быть числом" in str(messages)

    @allure.story("Тестирование обновления отзыва на несуществующий фильм")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_reviews_invalid_id(self, reviews_data, created_reviews, super_admin):
        with allure.step("Создаем переменную с несуществующим фильмом"):
            movie_id = -1
        with allure.step("Пытаемся обновить отзыв, на несуществующий фтльм"):
            response = super_admin.api.reviews_api.update_reviews(movie_id=movie_id, reviews_data=reviews_data, expected_status=404)
        with allure.step("Проверяем текст сообщения об ошибке"):
            response_data = response.json()
            assert response_data["message"] == "Отзыв не найден"

    @allure.story("Тестирование удаления отзыва")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.slow
    def test_delete_reviews(self, created_reviews, super_admin):
        with allure.step("Записываем в переменную фильм с отзывом"):
            movie_id = created_reviews
        with allure.step("Удаляем отзыв"):
            super_admin.api.reviews_api.delete_reviews(movie_id=movie_id)
        with allure.step("Проверяем что у фильма нет отзыва"):
            response = super_admin.api.reviews_api.get_reviews(movie_id=movie_id, expected_status=200)
            reviews = response.json()
            assert len(reviews) == 0

    @allure.story("Тестирование удаления уже удаленного отзыва")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_reviews_invalid_id(self, created_reviews, super_admin):
        with allure.step("Записываем в переменную фильм с отзывом"):
            movie_id = created_reviews
        with allure.step("Удаляем отзыв"):
            super_admin.api.reviews_api.delete_reviews(movie_id=movie_id)
        with allure.step("Пытаемся удалить уже удаленный отзыв"):
            response = super_admin.api.reviews_api.delete_reviews(movie_id=movie_id, expected_status=404)
        with allure.step("Проверяем что отзыв удален"):
            response_data = response.json()
            assert response_data["message"] == "Отзыв не найден"

    @allure.story("Тестирование получения отзыва")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_reviews(self, created_reviews, super_admin):
        with allure.step("Записываем в переменную фильм с отзывом"):
            movies_id = created_reviews
        with allure.step("Отправляем запрос для получения отзыва"):
            response = super_admin.api.reviews_api.get_reviews(movie_id=movies_id)
        with allure.step("Проверяем что получили искомый отзыв"):
            response_data = response.json()
            assert len(response_data) > 0
            firs_review = response_data[0]
            assert "text" in firs_review
            assert "rating" in firs_review

    @allure.story("Тестирование получения несуществующего отзыва")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_reviews_invalid_id(self, super_admin):
        with allure.step("Создаем переменную с несуществующим id фильма"):
            movies_id = -1
        with allure.step("Пытаемся получить несуществующий отзыв"):
            response = super_admin.api.reviews_api.get_reviews(movie_id=movies_id, expected_status=404)
        with allure.step("Проверяем текст ошибки"):
            response_data = response.json()
            assert response_data["message"] == "Фильм не найден"

    @allure.story("Тестирование получения удаленного отзыва")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_reviews_empty(self, created_reviews, super_admin):
        with allure.step("Записываем в переменную фильм с отзывом"):
            movies_id = created_reviews
        with allure.step("Удаляем отзыв"):
            super_admin.api.reviews_api.delete_reviews(movie_id=movies_id)
        with allure.step("Пытаемся получить отзыв к фильму"):
            response = super_admin.api.reviews_api.get_reviews(movie_id=movies_id)
        with allure.step("Проверяем что у фильма нет отзыва"):
            response_data = response.json()
            assert len(response_data) == 0
            assert response_data == []

    @allure.story("Тестирование включения отображения отзыва к фильму")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_show_reviews(self, created_reviews, auth_session, super_admin):
        with allure.step("Записываем в переменную фильм с отзывом"):
            movies_id = created_reviews
        with allure.step("Включаем отображение отзыва к фильму"):
            response = super_admin.api.reviews_api.show_review(movie_id=movies_id, user_Id=auth_session)
        with allure.step("Проверяем что поля есть в отзыве"):
            response_data = response.json()
            assert "text" in response_data
            assert "rating" in response_data

    @allure.story("Тестирование включения отображения отзыва к фильму, по несуществующему id")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_show_reviews_invalid_id(self, auth_session, super_admin):
        with allure.step("Создаем переменную с несуществующим id"):
            movie_data = -1
        with allure.step("Пытаемся включить отображение несуществующего отзыва"):
            response = super_admin.api.reviews_api.show_review(movie_id=movie_data, user_Id=auth_session, expected_status=404)
        with allure.step("Проверяем текст ошибки"):
            response_data = response.json()
            assert response_data["message"] == "Отзыв не найден"

    @allure.story("Тестирование отключения отображения отзыва к фильму")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_hide_reviews(self, created_reviews, auth_session, super_admin):
        with allure.step("Записываем в переменную фильм с отзывом"):
            movie_id = created_reviews
        with allure.step("Отключаем отображение отзыва к фильму"):
            response = super_admin.api.reviews_api.hide_review(movie_id=movie_id, user_Id=auth_session)
        with allure.step("Проверяем что поля есть в отзыве"):
            response_data = response.json()
            assert "text" in response_data
            assert "rating" in response_data

    @allure.story("Тестирование отключения отображения отзыва к фильму, по несуществующему id")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_hide_reviews_invalid_id(self, auth_session, super_admin):
        with allure.step("Создаем переменную с несуществующим id"):
            movie_data = -1
        with allure.step("Пытаемся отключить отображение несуществующего отзыва"):
            response = super_admin.api.reviews_api.hide_review(movie_id=movie_data, user_Id=auth_session, expected_status=404)
        with allure.step("Проверяем текст ошибки"):
            response_data = response.json()
            assert response_data["message"] == "Отзыв не найден"