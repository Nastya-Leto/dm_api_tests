import allure
import structlog

from chekers.http_chekers import check_status_kode_http

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])

@allure.suite('Тесты на проверку метода post_v1_account_token')
@allure.sub_suite('Проверка активации пользователя')
class TestActivationUser:

    @allure.title('Проверка успешной активации пользователя')
    def test_successful_activation_user(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        with check_status_kode_http():
            account_helper.register_new_user(login, password, email)
            account_helper.user_login(login, password)

    @allure.title('Проверка неуспешной активации пользователя, при отсутствии токена')
    def test_unsuccessful_activation_user(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        token = None
        account_helper.creating_new_user(login, password, email)
        with check_status_kode_http(expected_status_kode=400,
                                    expected_message='One or more validation errors occurred.'):
            account_helper.activation_user(token)
