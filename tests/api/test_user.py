from models.base_model import RegisterUserResponse

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        created_user = RegisterUserResponse(**response)

        assert created_user.id, "ID должен быть не пустым"
        assert created_user.email == creation_user_data.email
        assert created_user.fullName == creation_user_data.fullName
        assert created_user.roles == creation_user_data.roles
        assert created_user.verified is True
        assert created_user.banned is False

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        created_user = RegisterUserResponse.model_validate(created_user_response)
        user_by_id = super_admin.api.user_api.get_user(created_user.id).json()
        response_by_id = RegisterUserResponse.model_validate(user_by_id)
        response_email = super_admin.api.user_api.get_user(created_user.email).json()
        response_by_email = RegisterUserResponse(**response_email)

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.id and created_user.id , "ID должен совпадать"
        assert response_by_id.email == created_user.email
        assert response_by_id.fullName == created_user.fullName
        assert response_by_id.roles == created_user.roles
        assert created_user.verified is True
        assert created_user.banned is False

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    def test_get_user_id_admin_user(self, admin_user):
        admin_user.api.user_api.get_user(admin_user.email)