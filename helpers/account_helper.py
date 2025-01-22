from json import loads
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailhogApi
from retrying import retry

def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None

class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailhogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def creating_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        return response

    def activation_user(self, token):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    def register_new_user(self, login: str, password: str, email: str, with_activate: bool = True):
        # Создание пользователя
        response = self.creating_new_user(login, password, email)
        assert response.status_code == 201, f'Пользователь не был создан{response.text}'

        if with_activate:
            token = self.get_activation_token_by_login(login)
            response = self.activation_user(token)
        return response

    def user_login(self, login, password, remember_me: bool = True):

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data)
        return response

    def change_email_user(self, login, password, new_email):
        json_data = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        return response

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none,wait_fixed=1000)
    def get_activation_token_by_login(self,login):
        # Получение токена из письма
        token = None
        response = self.mailhog.mailhog_api.get_message_from_mail()
        resp_js = response.json()
        for item in resp_js['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                assert token is not None, 'Токен отсутствует'
        return token

    def get_new_activation_token(self, new_email):
        new_token = None
        response = self.mailhog.mailhog_api.get_message_from_mail()
        resp_js2 = response.json()
        for item in resp_js2['items']:
            json_headers = item['Content']['Headers']['To']
            new_email_from_message = ''.join(json_headers)
            if new_email_from_message == new_email:
                new_body = loads(item['Content']['Body'])
                new_token = new_body['ConfirmationLinkUrl'].split('/')[-1]
                return new_token





