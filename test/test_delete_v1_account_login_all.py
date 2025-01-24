def test_delete_v1_account_login_all(auth_account_helper_f):
    response = auth_account_helper_f.logout_all()
    assert response.status_code == 204