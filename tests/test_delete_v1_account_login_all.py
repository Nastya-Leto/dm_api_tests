import allure

from chekers.http_chekers import check_status_kode_http

@allure.suite('Тесты на проверку метода delete_v1_account_login_all')
@allure.title('Проверка выхода пользователя со всех устройств')
def test_delete_v1_account_login_all(auth_account_helper):
    with check_status_kode_http():
        response = auth_account_helper.logout_all()
