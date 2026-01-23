from custom_requester.custom_requester import CustomRequester
from constans import BASE_URL, MOVIE_ENDPOINT, REVIEW_ENDPOINT, HIDE_ENDPOINT, SHOW_ENDPOINT

class ReviewsAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session = session, base_url=BASE_URL)

    def create_reviews(self, movie_id, reviews_data,expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}/{REVIEW_ENDPOINT}",
            data=reviews_data,
            expected_status=expected_status
        )

    def delete_reviews(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}/{REVIEW_ENDPOINT}",
            expected_status=expected_status
        )

    def update_reviews(self, movie_id, reviews_data, expected_status=200):
        return self.send_request(
            method="PUT",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}/{REVIEW_ENDPOINT}",
            data=reviews_data,
            expected_status=expected_status
        )

    def get_reviews(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}/{REVIEW_ENDPOINT}",
            expected_status=expected_status
        )

    def hide_review(self, movie_id, user_Id, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}/{HIDE_ENDPOINT}/{user_Id}",
            expected_status=expected_status
        )

    def show_review(self, movie_id, user_Id, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}/{SHOW_ENDPOINT}/{user_Id}",
            expected_status=expected_status
        )