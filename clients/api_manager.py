from clients.auth_api import AuthAPI

class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
