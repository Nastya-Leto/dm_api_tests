from json import loads
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailhogApi
from retrying import retry

def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None

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
        token = self.get_activation_token_by_login(login)
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





