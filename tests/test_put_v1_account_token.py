import random
from json import loads

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailhogApi
from services.dm_api_account import DMApiAccount
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


class TestActivationUser:

    def test_successful_activation_user(self):
        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
        account = DMApiAccount(configuration=dm_api_configuration)
        mailhog = MailhogApi(configuration=mailhog_configuration)
        account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

        random_number = random.randint(1000, 2000)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'

        account_helper.register_new_user(login, password, email)
        account_helper.user_login(login, password)


    def test_unsuccessful_activation_user(self):

        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
        account = DMApiAccount(configuration=dm_api_configuration)
        mailhog = MailhogApi(configuration=mailhog_configuration)

        random_number = random.randint(2001, 3000)
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
        assert response.status_code == 201, f'Пользователь не был создан,{response.text}'
        print(response.text)

        # Получение письма из почты
        response = mailhog.mailhog_api.get_message_from_mail()
        print(response.status_code)
        assert response.status_code == 200, f'Письмо не было получено,{response.text}'
        # resp_js = response.json()

        # Активация пользователя
        token = None
        response = account.account_api.put_v1_account_token(token)
        assert response.status_code == 400, f'Успешная активация пользователя с пустым токеном,{response.text}'
        print(response.status_code)
        print(response.text)
