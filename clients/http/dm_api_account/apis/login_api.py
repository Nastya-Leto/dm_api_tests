from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


class LoginApi(RestClient):
    def post_v1_account_login(self, login_credentials: LoginCredentials,validate_response=True):
        """
        POST/v1/account/login
        Authenticate via credentials
        :param:
        :return:
        """
        response = self.post( path=f'/v1/account/login',
                              json=login_credentials.model_dump(exclude_none=True, by_alias=True))
        if validate_response:
            return UserEnvelope(**response.json())
        return response
