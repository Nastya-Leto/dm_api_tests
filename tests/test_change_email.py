from json import loads
from pprint import pprint

from api_mailhog.apis.mailhog_api import MailHogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
import random


class TestChangeEmail:
    def test_successful_change_email_user(self):
        account_api = AccountApi('http://5.63.153.31:5051')
        login_api = LoginApi('http://5.63.153.31:5051')
        mailhog_api = MailHogApi('http://5.63.153.31:5025')

        random_number = random.randint(100, 999)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'
        new_email = f'{login}New@mail.ru'

        # Создание пользователя
        json_data1 = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = account_api.create_user(json_data1)

        print(f'Создание пользователя {response.status_code},{response.text}')
        assert response.status_code == 201, 'Пользователь не был создан'

        # Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(f'Получение письма из почты {response.status_code},{response.text}')
        assert response.status_code == 200, 'Письма не были получены'
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
        assert token is not None, 'Токен не получен'

        # Активация пользователя
        response = account_api.activation_user(token)
        assert response.status_code == 200, 'Пользователь не был актививирован'
        print(f'Активация пользователя {response.status_code},{response.text}')

        # Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.authorization_user(json_data2)
        print(f'Авторизация пользователя {response.status_code},{response.text}')
        assert response.status_code == 200, 'Пользователь не был авторизован'

        # Изменение email
        json_data3 = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = account_api.change_email(json_data3)
        print(f'Смена email {response.status_code},{response.text}')

        # Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.authorization_user(json_data2)
        print(f'Авторизация пользователя {response.status_code},{response.text}')
        assert response.status_code == 403, 'Пользователь был авторизован, без повторной активации токена'

        # Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(f'Получение письма из почты {response.status_code},{response.text}')
        assert response.status_code == 200, 'Письмо не было получено'
        resp_js2 = response.json()

        new_token = None
        for item in resp_js2['items']:
            json_headers = item['Content']['Headers']['To']
            new_email_from_message = ''.join(json_headers)
            pprint(json_headers)
            if new_email_from_message == new_email:
                new_body = loads(item['Content']['Body'])
                new_token = new_body['ConfirmationLinkUrl'].split('/')[-1]

        # Повторная активация пользователя
        response = account_api.activation_user(new_token)
        assert response.status_code == 200, 'Пользователь был актививирован'
        print(f'Повторная активация пользователя {response.status_code},{response.text}')

        # Авторизация пользователя c новым email
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.authorization_user(json_data2)
        print(f'Получение авторизация пользователя {response.status_code},{response.text}')
        assert response.status_code == 200, 'Пользователь не был авторизован'

    def test_unsuccessful_change_email_user(self):
        account_api = AccountApi('http://5.63.153.31:5051')
        login_api = LoginApi('http://5.63.153.31:5051')
        mailhog_api = MailHogApi('http://5.63.153.31:5025')

        random_number = random.randint(100, 999)
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
        response = account_api.create_user(json_data1)

        print(f'Создание пользователя {response.status_code},{response.text}')
        assert response.status_code == 201, 'Пользователь не был создан'

        # 2 Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(f'Получение письма из почты {response.status_code},{response.text}')
        assert response.status_code == 200, 'Письмо не было получено'
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
        response = account_api.activation_user(token)
        assert response.status_code == 200, 'Пользователь не был актививирован'
        print(f'Активация пользователя {response.status_code},{response.text}')

        # 5 Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.authorization_user(json_data2)
        print(f'Авторизация пользователя {response.status_code},{response.text}')
        assert response.status_code == 200, 'Пользователь не был авторизован'

        # 6 смена email
        json_data3 = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = account_api.change_email(json_data3)
        assert response.status_code == 400, 'Успешное изменение email на невалидный'
        print(f'Смена email {response.status_code},{response.text}')
