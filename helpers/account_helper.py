import time
import allure
from json import loads

from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
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

    @allure.step('Авторизация клиента')
    def auth_client(self, login: str, password: str):
        response = self.user_login(login, password)
        token = {
            "x-dm-auth-token": response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    @allure.step('Создание нового пользователя')
    def creating_new_user(self, login: str, password: str, email: str):
        registration = Registration(
            login=login,
            email=email,
            password=password,
        )
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        return response

    @allure.step('Активация пользователя')
    def activation_user(self, token, validate_response=False):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token,
                                                                        validate_response=validate_response)
        return response

    @allure.step('Регистрация нового пользователя')
    def register_new_user(self, login: str, password: str, email: str, with_activate: bool = True):
        # Создание пользователя
        response = self.creating_new_user(login, password, email)

        if with_activate:
            token = self.get_activation_token_by_login(login)
            response = self.activation_user(token)
        return response

    @allure.step('Аутентификация пользователя в системе')
    def user_login(self, login, password, remember_me: bool = True, validate_response=False, validate_headers=False):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            rememberMe=remember_me,

        )
        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials,
                                                                       validate_response=validate_response)
        if validate_headers:
            assert response.headers['x-dm-auth-token'], f'Токен для пользователя не был получен'
        return response

    @allure.step('Смена email пользователя')
    def change_email_user(self, login, password, new_email, validate_response=True):
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=new_email)
        response = self.dm_account_api.account_api.put_v1_account_email(change_email,
                                                                        validate_response=validate_response)
        return response

    @allure.step('Сброс пароля пользователя')
    def reset_password(self, login, email):
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        self.dm_account_api.account_api.post_v1_account_password(reset_password)

    @allure.step('Смена пароля пользователя')
    def change_password(self, login, email, password, new_password):
        self.reset_password(login, email)
        token = self.get_token_reset(login)
        self.auth_client(login, password)

        change_password = ChangePassword(
            login=login,
            token=token,
            oldPassword=password,
            newPassword=new_password
        )
        response = self.dm_account_api.account_api.put_v1_account_password(change_password)
        return response

    @allure.step('Выход текущего пользователя из системы')
    def logout_current_user(self):
        response = self.dm_account_api.account_api.delete_v1_account_login()
        return response

    @allure.step('Выход пользователя со всех устройств')
    def logout_all(self):
        response = self.dm_account_api.account_api.delete_v1_account_login_all()
        return response

    @allure.step('Получение токена активации')
    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login):
        token = None
        start_time = time.time()
        response = self.mailhog.mailhog_api.get_message_from_mail()
        end_time = time.time()
        assert end_time - start_time < 3, f'Превышено время выполнения запроса'
        resp_js = response.json()
        for item in resp_js['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                assert token is not None, 'Токен отсутствует'
        return token

    @allure.step('Получение токена для смены email')
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

    @allure.step('Получение токена для сброса пароля')
    def get_token_reset(self, login):
        token = None
        response = self.mailhog.mailhog_api.get_message_from_mail()
        resp_js = response.json()
        for item in resp_js['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUri'].split('/')[-1]
                assert token is not None, 'Токен отсутствует'
        return token
