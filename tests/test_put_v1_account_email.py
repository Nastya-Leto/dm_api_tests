import structlog

from chekers.http_chekers import check_status_kode_http

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

        with check_status_kode_http(403, 'User is inactive. Address the technical support for more details'):
            account_helper.user_login(login, password)
            token = account_helper.get_new_activation_token(new_email=new_email)
            with check_status_kode_http:
                account_helper.activation_user(token=token)
                account_helper.user_login(login, password)

    def test_unsuccessful_change_email_user(self, account_helper, prepare_user, ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_email = f'{login}New.ru'
        message = {'Email': ['Invalid']}

        account_helper.register_new_user(login, password, email)
        account_helper.user_login(login, password)
        with check_status_kode_http(expected_status_kode=400, expected_message='Validation failed',
                                    expected_errors_message=message):
            account_helper.change_email_user(login, password, new_email, validate_response=False)
