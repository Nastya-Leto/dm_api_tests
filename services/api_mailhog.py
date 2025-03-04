from packages.restclient.configuration import Configuration
from clients.http.api_mailhog.apis.mailhog_api import MailHogApi


class MailhogApi:
    def __init__(self, configuration:Configuration):
        self.configuration = configuration
        self.mailhog_api = MailHogApi(configuration=self.configuration)
