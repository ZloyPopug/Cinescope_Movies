from conftest import api_manager
from clients.api_manager import ApiManager
from models.base_model import RegisterUserResponse


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(user_data=test_user)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"

    def test_login_user(self, api_manager: ApiManager, test_user,):
        register_response = api_manager.auth_api.register_user(user_data=test_user)
        register_user = RegisterUserResponse(**register_response.json())

        login_data = {
            "email": register_user.email,
            "password": test_user.password
        }
        login_response = api_manager.auth_api.login_user(login_data)
        login_response_data = login_response.json()
        assert login_response_data["user"]["email"] == register_user.email, "email не совпадает"
        assert login_response_data["user"]["id"] == register_user.id, "id не совпадает"
        assert login_response_data["user"]["fullName"] == register_user.fullName, "fullName не совпадает"
        assert login_response_data["user"]["roles"] == [role.value for role in register_user.roles], "roles не совпадают"
        assert "accessToken" in login_response_data, "Нет access token"
        assert "refreshToken" in login_response_data, "Нет refresh token"
        assert login_response_data["accessToken"], "access token пустой"
        assert login_response_data["refreshToken"], "refresh token пустой"


    def test_login_user_invalid_password(self, api_manager, test_user):
        register_response = api_manager.auth_api.register_user(user_data=test_user)
        register_user = RegisterUserResponse(**register_response.json())
        login_data_broken_password = {
            "email": register_user.email,
            "password": "123"
        }
        api_manager.auth_api.login_user(login_data_broken_password, expected_status=401)

    def test_login_user_invalid_email(self, api_manager, test_user):
        login_data_broken_email = {
            "email": "test@test.com",
            "password": test_user.password
        }
        api_manager.auth_api.login_user(login_data_broken_email, expected_status=401)

    def test_login_invalid_format_email(self, api_manager, test_user):
        login_data_invalid_email = {
            "email": "not-an-email",
            "password": "any_password"
        }
        api_manager.auth_api.login_user(login_data_invalid_email, expected_status=401)

    def test_login_empty_data(self, api_manager):
        api_manager.auth_api.login_user({}, expected_status=401)

