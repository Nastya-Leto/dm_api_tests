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
        assert response.status_code == 403, f'Пользователь был авторизован, без повторной активации токена{response.text}'

        token = account_helper.get_activation_token_by_login(login)
        account_helper.activation_user(token=token)
        response = account_helper.user_login(login, password)
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'


    def test_unsuccessful_change_email_user(self):
        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
        account = DMApiAccount(configuration=dm_api_configuration)
        mailhog = MailhogApi(configuration=mailhog_configuration)
        account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

        random_number = random.randint(4001, 5000)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'
        new_email = f'{login}New.ru'

        account_helper.register_new_user(login, password, email)
        account_helper.user_login(login, password)
        response = account_helper.change_email_user(login, password, new_email)
        assert response.status_code == 400, f'Успешное изменение email на невалидный{response.text}'

