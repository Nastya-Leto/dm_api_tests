import time
from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailhogApi
from retrying import retry


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f'Количество попыток{count}')
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError('Превышено количество попыток получения токена')
            if token:
                return token
            time.sleep(1)

    return wrapper



class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailhogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login: str, password: str):
        response = self.dm_account_api.login_api.post_v1_account_login(json_data={"login": login, 'password': password})
        token = {
            "x-dm-auth-token": response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)


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


    def reset_password(self, login, email):
        json_data = {
            "login": login,
            "email": email
        }
        self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)

    def change_password(self, login, email, password,new_password):

        self.reset_password(login, email)
        token = self.get_token_reset(login)
        self.auth_client(login,password)

        json_data = {
            "login": login,
            "token": token,
            "oldPassword": password,
            "newPassword": new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(json_data)
        return response

    def logout_current_user(self):
        response = self.dm_account_api.account_api.delete_v1_account_login()
        return response

    def logout_all(self):
        response = self.dm_account_api.account_api.delete_v1_account_login_all()
        return response

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login):
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

    @retrier
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

    def get_token_reset(self,login):
        token = None
        response = self.mailhog.mailhog_api.get_message_from_mail()
        resp_js = response.json()
        #pprint(resp_js)
        for item in resp_js['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUri'].split('/')[-1]
                assert token is not None, 'Токен отсутствует'
        return token
