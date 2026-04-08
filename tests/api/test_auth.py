import pytest

from conftest import api_manager
from clients.api_manager import ApiManager
from models.base_model import RegisterUserResponse
import allure

@allure.epic("Тестирование Аутентификации")
class TestAuthAPI:
    @allure.story("Тестирование регистрации пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_register_user(self, api_manager: ApiManager, test_user):
        with allure.step("Проводим Регистрацию пользователя"):
            response = api_manager.auth_api.register_user(user_data=test_user)
            register_user_response = RegisterUserResponse(**response.json())
        with allure.step("Проверяем что email юзера совпадает"):
            assert register_user_response.email == test_user.email, "Email не совпадает"

    @allure.story("Тестирование Атентификации пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_user(self, api_manager: ApiManager, test_user,):
        with allure.step("Проводим Регистрацию пользователя"):
            register_response = api_manager.auth_api.register_user(user_data=test_user)
            register_user = RegisterUserResponse(**register_response.json())
        with allure.step("Создаем переменную с данными для Аутентификации"):
            login_data = {
                "email": register_user.email,
                "password": test_user.password
            }
        with allure.step("Проводим Аутентификацию пользователя"):
            login_response = api_manager.auth_api.login_user(login_data)
            login_response_data = login_response.json()
        with allure.step("Проверяем есть ли основные поля"):
            assert login_response_data["user"]["email"] == register_user.email, "email не совпадает"
            assert login_response_data["user"]["id"] == register_user.id, "id не совпадает"
            assert login_response_data["user"]["fullName"] == register_user.fullName, "fullName не совпадает"
            assert login_response_data["user"]["roles"] == [role.value for role in register_user.roles], "roles не совпадают"
        with allure.step("Проверяем есть accessToken и refreshToken"):
            assert "accessToken" in login_response_data, "Нет access token"
            assert "refreshToken" in login_response_data, "Нет refresh token"
            assert login_response_data["accessToken"], "access token пустой"
            assert login_response_data["refreshToken"], "refresh token пустой"

    @allure.story("Тестирование Аутентификации с невалидным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_user_invalid_password(self, api_manager, test_user):
        with allure.step("Проводим Регистрацию пользователя"):
            register_response = api_manager.auth_api.register_user(user_data=test_user)
            register_user = RegisterUserResponse(**register_response.json())
        with allure.step("Создаем переменную с данными для Аутентификации и невалидными паролем"):
            login_data_broken_password = {
                "email": register_user.email,
                "password": "123"
            }
        with allure.step("Проводим Аутентификацию пользователя с невалидными паролем"):
            api_manager.auth_api.login_user(login_data_broken_password, expected_status=401)

    @allure.story("Тестирование Аутентификации с невалидным email")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_user_invalid_email(self, api_manager, test_user):
        with allure.step("Создаем переменную с данными для Аутентификации и невалидными email"):
            login_data_broken_email = {
                "email": "test@test.com",
                "password": test_user.password
            }
        with allure.step("Проводим Аутентификацию пользователя с невалидным email"):
            api_manager.auth_api.login_user(login_data_broken_email, expected_status=401)

    @allure.story("Тестирование Аутентификации с невалидным форматом email")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_invalid_format_email(self, api_manager, test_user):
        with allure.step("Создаем переменную с данными для Аутентификации с невалидными форматом email"):
            login_data_invalid_email = {
                "email": "not-an-email",
                "password": "any_password"
            }
        with allure.step("Проводим Аутентификацию пользователя с невалидными форматом email"):
            api_manager.auth_api.login_user(login_data_invalid_email, expected_status=401)

    @allure.story("Тестирование Аутентификации с пустым набором данных")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_empty_data(self, api_manager):
        with allure.step("Проводим Аутентификацию пользователя с пустым набором данных"):
            api_manager.auth_api.login_user({}, expected_status=401)

