import requests


class MailHogApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def get_message_from_mail(self, limit=2):
        """
        Get users emails
        :return:
        """
        params = {
            'limit': limit,
        }
        response = requests.get(
            url=f'{self.host}/api/v2/messages',
            params=params, verify=False)
        return response
