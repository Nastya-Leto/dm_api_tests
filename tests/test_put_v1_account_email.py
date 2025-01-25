import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


class TestChangeEmail:
    def test_successful_change_email_user(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_email = f'{login}New@mail.ru'

        account_helper.register_new_user(login, password, email)
        account_helper.user_login(login, password)
        account_helper.change_email_user(login, password, new_email)
        response = account_helper.user_login(login, password)
        assert response.status_code == 403, f'Пользователь был авторизован, без повторной активации токена{response.text}'

        token = account_helper.get_new_activation_token(new_email=new_email)
        account_helper.activation_user(token=token)
        response = account_helper.user_login(login, password)
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'


    def test_unsuccessful_change_email_user(self, account_helper, prepare_user):

        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_email = f'{login}New.ru'

        account_helper.register_new_user(login, password, email)
        account_helper.user_login(login, password)
        response = account_helper.change_email_user(login, password, new_email)
        assert response.status_code == 400, f'Успешное изменение email на невалидный{response.text}'

