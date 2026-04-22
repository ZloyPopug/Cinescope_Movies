from models.base_model import RegisterUserResponse
import allure
import pytest

@allure.epic("Тестирование Юзера")
class TestUser:

    @allure.story("Тестирование создания пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_user(self, super_admin, creation_user_data):
        with allure.step("Создаем пользователя"):
            response = super_admin.api.user_api.create_user(creation_user_data).json()
            created_user = RegisterUserResponse(**response)
        with allure.step("Проверяем данные созданного пользователя"):
            assert created_user.id, "ID должен быть не пустым"
            assert created_user.email == creation_user_data.email
            assert created_user.fullName == creation_user_data.fullName
            assert created_user.roles == creation_user_data.roles
            assert created_user.verified is True
            assert created_user.banned is False

    @allure.story("Тестирование получения пользователя по ID и email")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        with allure.step("Создаем пользователя"):
            created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
            created_user = RegisterUserResponse.model_validate(created_user_response)
        with allure.step("Получаем пользователя по id"):
            user_by_id = super_admin.api.user_api.get_user(created_user.id).json()
            response_by_id = RegisterUserResponse.model_validate(user_by_id)
        with allure.step("Получаем пользователя по email"):
            response_email = super_admin.api.user_api.get_user(created_user.email).json()
            response_by_email = RegisterUserResponse(**response_email)
        with allure.step("Сравниваем ответы"):
            assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
            assert response_by_id.id and created_user.id , "ID должен совпадать"
            assert response_by_id.email == created_user.email
            assert response_by_id.fullName == created_user.fullName
            assert response_by_id.roles == created_user.roles
            assert created_user.verified is True
            assert created_user.banned is False

    @allure.story("Тестирование получения пользователя с правами common_user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user_by_id_common_user(self, common_user):
        with allure.step("Пытаемся получить пользователя с правами common_user"):
            common_user.api.user_api.get_user(common_user.email, expected_status=403)

    @allure.story("Тестирование получения пользователя с правами admin_user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergey Guldeev")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user_id_admin_user(self, admin_user):
        with allure.step("Пытаемся получить пользователя с правами admin_user"):
            admin_user.api.user_api.get_user(admin_user.email)