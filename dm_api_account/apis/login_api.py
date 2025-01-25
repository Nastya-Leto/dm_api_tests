from dm_api_account.models.login_credentials import LoginCredentials
from restclient.client import RestClient


class LoginApi(RestClient):
    def post_v1_account_login(self, login_credentials: LoginCredentials):
        """
        POST/v1/account/login
        Authenticate via credentials
        :param:
        :return:
        """
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True))
        return response
