from json import loads
from pprint import pprint

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailhogApi
from services.dm_api_account import DMApiAccount
import random
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


class TestChangeEmail:
    def test_successful_change_email_user(self):
        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
        account = DMApiAccount(configuration=dm_api_configuration)
        mailhog = MailhogApi(configuration=mailhog_configuration)
        account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

        random_number = random.randint(3001, 4000)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'
        new_email = f'{login}New@mail.ru'

        account_helper.register_new_user(login, password, email)
        account_helper.user_login(login, password)
        account_helper.change_email_user(login, password, new_email)
        response = account_helper.user_login(login, password)
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'

    def test_unsuccessful_change_email_user(self):
        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
        account = DMApiAccount(configuration=dm_api_configuration)
        mailhog = MailhogApi(configuration=mailhog_configuration)

        random_number = random.randint(4001, 5000)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'
        new_email = f'{login}New.ru'

        # 1 Создание пользователя
        json_data1 = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = account.account_api.post_v1_account(json_data1)
        assert response.status_code == 201, f'Пользователь не был создан {response.text}'

        # 2 Получение письма из почты
        response = mailhog.mailhog_api.get_message_from_mail()
        assert response.status_code == 200, f'Письмо не было получено{response.text}'
        resp_js = response.json()

        # 3 Получение токена из письма
        token = None
        for item in resp_js['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        assert token is not None, 'Токен не получен'

        # 4 Активация пользователя
        response = account.account_api.put_v1_account_token(token)
        assert response.status_code == 200, f'Пользователь не был актививирован{response.text}'

        # 5 Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = account.login_api.post_v1_account_login(json_data2)
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'

        # 6 смена email
        json_data3 = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = account.account_api.put_v1_account_email(json_data3)
        assert response.status_code == 400, f'Успешное изменение email на невалидный{response.text}'
