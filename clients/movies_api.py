
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