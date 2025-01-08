from json import loads
import random

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailHogApi


class TestLoginUser:
    def test_successful_login(self):

        account_api = AccountApi('http://5.63.153.31:5051')
        login_api = LoginApi('http://5.63.153.31:5051')
        mailhog_api = MailHogApi('http://5.63.153.31:5025')

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

        # Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(response.status_code)
        assert response.status_code == 200, 'Письмо не было получено'
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

        # Активация пользователя
        response = account_api.activation_user(token)
        print(response.status_code)
        print(response.text)

        # Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.authorization_user(json_data2)
        print(response.status_code)
        assert response.status_code == 200, 'Пользователь не был авторизован'
        print(response.text)

    def test_unsuccessful_login(self):

        account_api = AccountApi('http://5.63.153.31:5051')
        login_api = LoginApi('http://5.63.153.31:5051')
        mailhog_api = MailHogApi('http://5.63.153.31:5025')

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

        # Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(response.status_code)
        assert response.status_code == 200, 'Письмо не было получено'
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

        response = login_api.authorization_user(json_data2)
        print(response.status_code)
        assert response.status_code == 403, 'Пользователь был авторизован без активации'
        print(response.text)
