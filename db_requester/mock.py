class EmailService:
    def send_email(self, to, subject, body):
        # Реальный код для отправки email
        pass


from unittest.mock import Mock


def test_send_email():
    email_service = Mock()
    email_service.send_password()

    email_service.send_password.assert_called()
