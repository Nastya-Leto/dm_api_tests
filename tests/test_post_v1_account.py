import allure
import structlog
import pytest

from chekers.http_chekers import check_status_kode_http

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])

@allure.suite('Тесты на проверку метода post_v1_account')
@allure.sub_suite('Проверка  создания пользователя')
class TestCreateUser:
    @allure.title('Проверка успешного создания пользователя')
    def test_successful_creation_user(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        with check_status_kode_http():
            account_helper.register_new_user(login, password, email)
            account_helper.user_login(login, password)

    @allure.title('Проверка невозможности создания пользователя с невалидными данными')
    @pytest.mark.parametrize("login, email, password, message",
                             [('a', 'zakharova@mail.ru', '123456789', {'Login': ['Short']}),
                              ('zakharova', 'zakharova.ru', '123456789', {'Email': ['Invalid']}),
                              ('zakharova', 'zakharova@mail.ru', '1', {'Password': ['Short']})])
    def test_negative_parametrized(self, account_helper, login, email, password, message):
        login = login
        email = email
        password = password
        with check_status_kode_http(expected_status_kode=400, expected_message='Validation failed',
                                    expected_errors_message=message):
            account_helper.creating_new_user(login, password, email)
