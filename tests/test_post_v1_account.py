import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


class TestCreateUser:
    def test_successful_creation_user(self, account_helper_f, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        response = account_helper_f.register_new_user(login, password, email)
        assert response.status_code == 200, f'Пользователь не был создан{response.text}'

        response = account_helper_f.user_login(login, password)
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'

    def test_creating_user_with_invalid_email(self, account_helper_f, prepare_user):

        login = prepare_user.login
        email = f'{login}.ru'
        password = prepare_user.password

        response = account_helper_f.creating_new_user(login, password, email)
        assert response.status_code == 400, f'Пользователь был создан c невалидным email {response.text}'
