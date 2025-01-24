

def test_get_v1_account_auth(auth_account_helper_f):
    auth_account_helper_f.dm_account_api.account_api.get_v1_account()

def test_get_v1_account_not_auth(account_helper_f):
    account_helper_f.dm_account_api.account_api.get_v1_account()
