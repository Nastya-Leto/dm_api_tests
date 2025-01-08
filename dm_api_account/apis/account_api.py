import requests


class AccountApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def create_user(self, json_data):
        """
        POST/v1/account
        Register new user
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data)
        return response

    def activation_user(self, token):
        """
        PUT/v1/account/{token}
        Activate registered user
        :param token:
        :return:
        """
        response = requests.put(
            url=f'{self.host}/v1/account/{token}')
        return response

    def change_email(self, json_data):
        """
        PUT/v1/account/email
        Change registered user email
        :return:
        """
        response = requests.put(
            url=f'{self.host}/v1/account/email',
            json=json_data
        )
        return response
