from collections import namedtuple
from datetime import datetime
import random

import pytest
from requests import session

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailhogApi
from services.dm_api_account import DMApiAccount
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailhogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper_f(mailhog_api, account_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture(scope="session")
def auth_account_helper_f(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(login="aazakharova17",password='123456789')
    return account_helper

@pytest.fixture()
def prepare_user():
    random_number = random.randint(5001, 6000)
    now = datetime.now()
    data = now.strftime('%d_%m_%Y_%H_%M_%S')
    login = f'aanastya{data}+{random_number}'
    email = f'{login}@mail.ru'
    password = '123456789'
    User = namedtuple('User',['login','password','email'])
    user = User(login=login,password=password,email=email)
    return user
