from restclient.client import RestClient


class MailHogApi(RestClient):
    def get_message_from_mail(self, limit=1):
        """
        Get users emails
        :return:
        """
        params = {
            'limit': limit,
        }
        response = self.get(
            path=f'/api/v2/messages',
            params=params, verify=False)
        return response
