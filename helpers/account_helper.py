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
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'
        return response


    def user_login(self,login,password, remember_me:bool=True):

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data)
        return response

    def change_email_user(self,login,password,new_email):
        # Изменение email
        json_data = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, f'Неуспешное изменение email {response.text}'


        # авторизация после смены email
        response = self.user_login(login, password)
        assert response.status_code == 403, f'Пользователь был авторизован, без повторной активации токена{response.text}'
        new_token = self.get_new_activation_token(new_email=new_email)
        # Повторная активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(new_token)
        assert response.status_code == 200, f'Пользователь был актививирован{response.text}'

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

    def get_new_activation_token(self,new_email):
        new_token = None
        # Получение письма из почты
        response = self.mailhog.mailhog_api.get_message_from_mail()
        resp_js2 = response.json()
        for item in resp_js2['items']:
            json_headers = item['Content']['Headers']['To']
            new_email_from_message = ''.join(json_headers)
            if new_email_from_message == new_email:
                new_body = loads(item['Content']['Body'])
                new_token = new_body['ConfirmationLinkUrl'].split('/')[-1]
                return new_token





