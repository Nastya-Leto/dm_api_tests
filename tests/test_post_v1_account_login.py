from json import loads
import random

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailhogApi
from services.dm_api_account import DMApiAccount
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


class TestLoginUser:
    def test_successful_login(self):
        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
        account = DMApiAccount(configuration=dm_api_configuration)
        mailhog = MailhogApi(configuration=mailhog_configuration)
        account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

        random_number = random.randint(7001, 8000)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'

        account_helper.register_new_user(login, password, email)
        response = account_helper.user_login(login, password)
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'

    def test_unsuccessful_login(self):

        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
        account = DMApiAccount(configuration=dm_api_configuration)
        mailhog = MailhogApi(configuration=mailhog_configuration)

        random_number = random.randint(8003, 9000)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'

        # Создание пользователя
        json_data1 = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = account.account_api.post_v1_account(json_data1)

        print(response.status_code)
        assert response.status_code == 201, f'Пользователь не был создан{response.text}'
        print(response.text)

        # Получение письма из почты
        response = mailhog.mailhog_api.get_message_from_mail()
        print(response.status_code)
        assert response.status_code == 200, f'Письмо не было получено{response.text}'
        resp_js = response.json()

        # Получение токена из письма
        token = None
        for item in resp_js['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                print(user_login)
                print(token)
        assert token is not None, 'Токен отсутствует'

        # Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = account.login_api.post_v1_account_login(json_data2)
        print(response.status_code)
        assert response.status_code == 403, f'Пользователь был авторизован без активации{response.text}'
        print(response.text)
