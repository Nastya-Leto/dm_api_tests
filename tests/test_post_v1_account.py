import structlog

from chekers.http_chekers import check_status_kode_http

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


class TestCreateUser:
    def test_successful_creation_user(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        with check_status_kode_http():
            account_helper.register_new_user(login, password, email)
            account_helper.user_login(login, password)

    def test_creating_user_with_invalid_email(self, account_helper, prepare_user):
        login = prepare_user.login
        email = f'{login}.ru'
        password = prepare_user.password
        with check_status_kode_http(expected_status_kode=400, expected_message='Validation failed'):
            account_helper.creating_new_user(login, password, email)
