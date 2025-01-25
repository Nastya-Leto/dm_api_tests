from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration):
        """
        POST/v1/account
        Register new user
        :param:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True))
        return response

    def get_v1_account(self, **kwargs):
        """
        GET/v1/account
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account/password',
            **kwargs)
        return response

    def put_v1_account_password(self, change_password: ChangePassword):
        """
        PUT/v1/account/password
        Change registered user password
        :param :
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True))
        return response

    def post_v1_account_password(self, reset_password: ResetPassword):
        """
        POST/v1/account/password
        Reset registered user password
        :param :
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True))
        return response

    def put_v1_account_token(self, token):
        """
        PUT/v1/account/{token}
        Activate registered user
        :param token:
        :return:
        """
        response = self.put(
            path=f'/v1/account/{token}')
        return response

    def put_v1_account_email(self, change_email: ChangeEmail):
        """
        PUT/v1/account/email
        Change registered user email
        :return:
        """
        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def delete_v1_account_login(self):
        """
        DELETE/v1/account/login
        Logout as current user
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login'
        )
        return response

    def delete_v1_account_login_all(self):
        """
        DELETE/v1/account/login/all
        Logout from every device
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login/all'
        )
        return response
