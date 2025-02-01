from chekers.get_v1_account import GetV1Account
from chekers.http_chekers import check_status_kode_http


def test_get_v1_account_auth(auth_account_helper):
    with check_status_kode_http():
        response = auth_account_helper.dm_account_api.account_api.get_v1_account()
        GetV1Account.check_response_value(response)


def test_get_v1_account_not_auth(account_helper):
    with check_status_kode_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
