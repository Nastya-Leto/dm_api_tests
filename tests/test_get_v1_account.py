import allure

from chekers.get_v1_account import GetV1Account
from chekers.http_chekers import check_status_kode_http

@allure.suite('Тесты на проверку метода get_v1_account_auth')
@allure.sub_suite('Тесты на проверку получения информации пользователя')
class TestGetUser:
    @allure.title('Проверка получения информации о пользователя')
    def test_get_v1_account_auth(self,auth_account_helper):
        with check_status_kode_http():
            response = auth_account_helper.dm_account_api.account_api.get_v1_account()
            GetV1Account.check_response_value(response)


    @allure.title('Проверка невозможности получения информации о пользователя без авторизации')
    def test_get_v1_account_not_auth(self,account_helper):
        with check_status_kode_http(401, 'User must be authenticated'):
            account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
