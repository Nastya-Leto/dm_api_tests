import allure

from chekers.http_chekers import check_status_kode_http
from chekers.post_v1_account_login import PostV1AccountLogin

@allure.suite('Тесты на проверку метода post_v1_account_login')
@allure.sub_suite('Проверка аутентификации пользователя')
class TestLoginUser:
    @allure.title('Проверка успешной аутентификации пользователя')
    def test_successful_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        with check_status_kode_http():
            account_helper.register_new_user(login, password, email)
            response = account_helper.user_login(login, password, validate_response=True)
            PostV1AccountLogin.check_response_value(response)

    @allure.title('Проверка неуспешной аутентификации пользователя, при отсутствии активации')
    def test_unsuccessful_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login, password, email, with_activate=False)

        with check_status_kode_http(403, 'User is inactive. Address the technical support for more details'):
            account_helper.user_login(login, password, validate_headers=False)
