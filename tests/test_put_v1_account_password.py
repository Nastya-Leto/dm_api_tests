
def test_put_v1_account_password(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = prepare_user.new_password


    account_helper.register_new_user(login, password, email)
    account_helper.user_login(login, password)
    account_helper.change_password(login, email, password, new_password)
    response = account_helper.user_login(login, new_password)
    assert response.status_code==200, f'Неудачная авторизация с новым паролем'

