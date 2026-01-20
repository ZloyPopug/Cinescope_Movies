from custom_requester.custom_requester import CustomRequester
from constans import BASE_URL,MOVIE_ENDPOINT

class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session = session, base_url=BASE_URL)

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method='POST',
            endpoint=MOVIE_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method='DELETE',
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method='GET',
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def update_movie(self, movie_id, movie_data, expected_status=200):
        return self.send_request(
            method='PATCH',
            endpoint=f'{MOVIE_ENDPOINT}/{movie_id}',
            data=movie_data,
            expected_status=expected_status
        )

    def get_movies_with_filters(self, params=None, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            params=params,
            expected_status=expected_status
        )