
def test_delete_v1_account_login(auth_account_helper_f):
    response = auth_account_helper_f.logout_current_user()
    assert response.status_code == 204