from chekers.http_chekers import check_status_kode_http


def test_delete_v1_account_login(auth_account_helper):
    with check_status_kode_http():
        auth_account_helper.logout_current_user()
