import random
from dm_api_account.apis.account_api import AccountApi


class TestCreateUser:
    def test_successful_creation_user(self):
        account_api = AccountApi('http://5.63.153.31:5051')

        random_number = random.randint(100, 999)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'

        # Создание пользователя
        json_data1 = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = account_api.create_user(json_data1)

        print(response.status_code)
        assert response.status_code == 201, 'Пользователь не был создан'
        print(response.text)

    def test_unsuccessful_creation_user(self):
        account_api = AccountApi('http://5.63.153.31:5051')

        random_number = random.randint(100, 999)
        login = f'aanastya{random_number}'
        email = f'{login}.ru'
        password = '123456789'

        # Создание пользователя
        json_data1 = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = account_api.create_user(json_data1)

        print(response.status_code)
        assert response.status_code == 400, f'Пользователь был создан c невалидным email {response.text}'
        print(response.text)
