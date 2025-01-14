import random
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


class TestCreateUser:
    def test_successful_creation_user(self):
        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        account = DMApiAccount(configuration=dm_api_configuration)

        random_number = random.randint(5001, 6000)
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

    def test_unsuccessful_creation_user(self):
        dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
        account = DMApiAccount(configuration=dm_api_configuration)

        random_number = random.randint(6001, 7000)
        login = f'aanastya{random_number}'
        email = f'{login}.ru'
        password = '123456789'

        # Создание пользователя
        json_data1 = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = account.account_api.post_v1_account(json_data1)

        print(response.status_code)
        assert response.status_code == 400, f'Пользователь был создан c невалидным email {response.text}'
        print(response.text)
