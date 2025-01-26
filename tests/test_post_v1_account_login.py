class TestLoginUser:
    def test_successful_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login, password, email)
        response = account_helper.user_login(login, password)
        assert response.headers['x-dm-auth-token'], f'Токен для пользователя не был получен'

    def test_unsuccessful_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        response = account_helper.register_new_user(login, password, email, with_activate=False)
        assert response.status_code == 201, f'Пользователь не был создан{response.text}'

        response = account_helper.user_login(login, password)
        assert response.status_code == 403, f'Пользователь был авторизован без активации{response.text}'
