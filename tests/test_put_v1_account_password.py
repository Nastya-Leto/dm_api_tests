import allure

from chekers.http_chekers import check_status_kode_http

@allure.suite('Тесты на проверку метода post_v1_account_password')
@allure.title('Проверка успешной смены пароля пользователя')
def test_put_v1_account_password(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = prepare_user.new_password

    account_helper.register_new_user(login, password, email)
    account_helper.user_login(login, password)
    account_helper.change_password(login, email, password, new_password)
    with check_status_kode_http():
        account_helper.user_login(login, new_password)
