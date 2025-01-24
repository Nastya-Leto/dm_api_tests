from restclient.client import RestClient


class AccountApi(RestClient):
main
    def post_v1_account(self, json_data):
        """
        POST/v1/account
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data)
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

    def put_v1_account_email(self, json_data):
        """
        PUT/v1/account/email
        Change registered user email
        :return:
        """
        response = self.put(
            path=f'/v1/account/email',
            json=json_data
        )
        return response
