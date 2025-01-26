import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


class TestActivationUser:

    def test_successful_activation_user(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login, password, email)
        account_helper.user_login(login, password)

    def test_unsuccessful_activation_user(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        token = None

        response = account_helper.creating_new_user(login, password, email)
        assert response.status_code == 201, f'Пользователь не был создан,{response.text}'

        response = account_helper.activation_user(token)
        assert response.status_code == 400, f'Успешная активация пользователя с пустым токеном,{response.text}'
