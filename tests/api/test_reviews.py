from clients.api_manager import ApiManager

class TestReviews:
    def test_create_reviews(self, created_movie, reviews_data, api_manager:ApiManager):
        movie_id = created_movie["id"]
        response = api_manager.reviews_api.create_reviews(movie_id=movie_id, reviews_data=reviews_data)
        response_data = response.json()
        assert response_data["text"] == reviews_data["text"]
        assert response_data["rating"] == reviews_data["rating"]

    def test_create_reviews_invalid_value(self, created_movie, api_manager:ApiManager):
        movie_id = created_movie["id"]
        invalid_data = {
            "rating": "test",
            "text": 123
        }
        api_manager.reviews_api.create_reviews(movie_id=movie_id, reviews_data=invalid_data, expected_status=400)


    def test_create_reviews_invalid_id(self, reviews_data, auth_session, api_manager:ApiManager):
        movie_id = -1
        api_manager.reviews_api.create_reviews(movie_id=movie_id,reviews_data=reviews_data,expected_status=404)


    def test_create_reviews_already_exists(self, created_reviews, reviews_data, api_manager:ApiManager):
        movie_id = created_reviews
        response = api_manager.reviews_api.create_reviews(movie_id=movie_id, reviews_data=reviews_data, expected_status=409)
        response_data = response.json()
        assert response_data["message"] == "Вы уже оставляли отзыв к этому фильму"

    def test_update_reviews(self,created_reviews, reviews_data, api_manager:ApiManager):
        movie_id = created_reviews
        response = api_manager.reviews_api.update_reviews(movie_id=movie_id, reviews_data=reviews_data)
        response_data = response.json()
        assert response_data["text"] == reviews_data["text"]
        assert response_data["rating"] == reviews_data["rating"]
        assert response_data["movieId"] == movie_id
        assert "userId" in response_data
        assert "hidden" in response_data
        assert "createdAt" in response_data

    def test_update_reviews_invalid_value(self, created_reviews, api_manager:ApiManager):
        movie_id = created_reviews
        invalid_data = {
            "rating": "test",
            "text": 123
        }
        api_manager.reviews_api.update_reviews(movie_id=movie_id, reviews_data=invalid_data, expected_status=400)

    def test_update_reviews_invalid_id(self, reviews_data, created_reviews, api_manager:ApiManager):
        movie_id = -1
        api_manager.reviews_api.update_reviews(movie_id=movie_id, reviews_data=reviews_data, expected_status=404)

    def test_delete_reviews(self, created_reviews, api_manager:ApiManager):
        movie_id = created_reviews
        api_manager.reviews_api.delete_reviews(movie_id=movie_id)
        response = api_manager.reviews_api.get_reviews(movie_id=movie_id, expected_status=200)
        reviews = response.json()
        assert len(reviews) == 0

    def test_delete_reviews_invalid_id(self, created_reviews, api_manager:ApiManager):
        movie_id = created_reviews
        api_manager.reviews_api.delete_reviews(movie_id=movie_id)
        response = api_manager.reviews_api.delete_reviews(movie_id=movie_id, expected_status=404)
        response_data = response.json()
        assert response_data["message"] == "Отзыв не найден"

    def test_get_reviews(self, created_reviews, api_manager:ApiManager):
        movies_id = created_reviews
        response = api_manager.reviews_api.get_reviews(movie_id=movies_id)
        response_data = response.json()
        assert len(response_data) > 0
        firs_review = response_data[0]
        assert "text" in firs_review
        assert "rating" in firs_review

    def test_get_reviews_invalid_id(self, api_manager:ApiManager):
        movies_id = -1
        response = api_manager.reviews_api.get_reviews(movie_id=movies_id, expected_status=404)
        response_data = response.json()
        assert response_data["message"] == "Фильм не найден"

    def test_get_reviews_empty(self, created_reviews, api_manager:ApiManager):
        movies_id = created_reviews
        api_manager.reviews_api.delete_reviews(movie_id=movies_id)
        response = api_manager.reviews_api.get_reviews(movie_id=movies_id)
        response_data = response.json()
        assert len(response_data) == 0
        assert response_data == []

    def test_show_reviews(self, created_reviews, auth_session, api_manager:ApiManager):
        movies_id = created_reviews
        response = api_manager.reviews_api.show_review(movie_id=movies_id, user_Id=auth_session)
        response_data = response.json()
        assert "text" in response_data
        assert "rating" in response_data

    def test_show_reviews_invalid_id(self, auth_session, api_manager:ApiManager):
        movie_data = -1
        response = api_manager.reviews_api.show_review(movie_id=movie_data, user_Id=auth_session, expected_status=404)
        response_data = response.json()
        assert response_data["message"] == "Отзыв не найден"

    def test_hide_reviews(self, created_reviews, auth_session, api_manager:ApiManager):
        movie_id = created_reviews
        response = api_manager.reviews_api.hide_review(movie_id=movie_id, user_Id=auth_session)
        response_data = response.json()
        assert "text" in response_data
        assert "rating" in response_data

    def test_hide_reviews_invalid_id(self, auth_session, api_manager:ApiManager):
        movie_data = -1
        response = api_manager.reviews_api.hide_review(movie_id=movie_data, user_Id=auth_session, expected_status=404)
        response_data = response.json()
        assert response_data["message"] == "Отзыв не найден"