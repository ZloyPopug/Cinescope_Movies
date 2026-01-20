from requests import session

from constans import LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester

class AuthAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url = "https://auth.dev-cinescope.coconutqa.ru/")

    def login_user(self, user_data, expected_status=200):
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def authenticate(self):
        login_data = {
            "email": "api1@gmail.com",
            "password": "asdqwe123Q"
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})