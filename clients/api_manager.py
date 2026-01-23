from clients.auth_api import AuthAPI
from clients.movies_api import MoviesAPI
from clients.reviews_api import ReviewsAPI


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.movies_api = MoviesAPI(session)
        self.reviews_api = ReviewsAPI(session)
