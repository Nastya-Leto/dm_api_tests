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


class TestCreateUser:
    def test_successful_creation_user(self):
        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
        account = DMApiAccount(configuration=dm_api_configuration)
        mailhog = MailhogApi(configuration=mailhog_configuration)
        account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

        random_number = random.randint(5001, 6000)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'


        response = account_helper.register_new_user(login, password, email)
        assert response.status_code == 200, f'Пользователь не был создан{response.text}'

        response = account_helper.user_login(login, password)
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'

    def test_creating_user_with_invalid_email(self):
        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
        account = DMApiAccount(configuration=dm_api_configuration)
        mailhog = MailhogApi(configuration=mailhog_configuration)
        account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)


        random_number = random.randint(6001, 7000)
        login = f'aanastya{random_number}'
        email = f'{login}.ru'
        password = '123456789'

        response = account_helper.creating_new_user(login, password, email)
        assert response.status_code == 400, f'Пользователь был создан c невалидным email {response.text}'
