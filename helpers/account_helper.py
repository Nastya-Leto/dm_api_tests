from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailhogApi

class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog:MailhogApi):
        self.dm_account_api = dm_account_api
        self.mailhog=mailhog

    def register_new_user(self,login:str, password:str, email:str):
        # Создание пользователя
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data)
        assert response.status_code == 201, f'Пользователь не был создан{response.text}'

        response = self.mailhog.mailhog_api.get_message_from_mail()
        assert response.status_code == 200, f'Письмо не было получено{response.text}'

        token = self.get_activation_token_by_login(login,response)
        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token)
        return response

    def user_login(self,login,password, remember_me:bool=True):

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data)

        return response

    @staticmethod
    def get_activation_token_by_login(login, response):
        # Получение токена из письма
        token = None
        resp_js = response.json()
        for item in resp_js['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                assert token is not None, 'Токен отсутствует'
        return token





