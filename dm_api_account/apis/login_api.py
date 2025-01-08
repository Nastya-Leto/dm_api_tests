import requests


class LoginApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def authorization_user(self, json_data):
        """
        POST/v1/account/login
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account/login',
            json=json_data)
        return response
