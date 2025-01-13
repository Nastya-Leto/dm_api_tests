from json import loads
from pprint import pprint

from api_mailhog.apis.mailhog_api import MailHogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
import random
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)])


class TestChangeEmail:
    def test_successful_change_email_user(self):
        account_api = AccountApi('http://5.63.153.31:5051')
        login_api = LoginApi('http://5.63.153.31:5051')
        mailhog_api = MailHogApi('http://5.63.153.31:5025')

        random_number = random.randint(3001, 4000)
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
        response = account_api.post_v1_account(json_data1)

        print(f'Создание пользователя {response.status_code},{response.text}')
        assert response.status_code == 201, f'Пользователь не был создан,{response.text}'

        # Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(f'Получение письма из почты {response.status_code},{response.text}')
        assert response.status_code == 200, f'Письма не были получены,{response.text}'
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
        response = account_api.put_v1_account_token(token)
        assert response.status_code == 200, f'Пользователь не был актививирован{response.text}'
        print(f'Активация пользователя {response.status_code},{response.text}')

        # Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.post_v1_account_login(json_data2)
        print(f'Авторизация пользователя {response.status_code},{response.text}')
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'

        # Изменение email
        json_data3 = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = account_api.put_v1_account_email(json_data3)
        print(f'Смена email {response.status_code},{response.text}')

        # Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.post_v1_account_login(json_data2)
        print(f'Авторизация пользователя {response.status_code},{response.text}')
        assert response.status_code == 403, f'Пользователь был авторизован, без повторной активации токена{response.text}'

        # Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(f'Получение письма из почты {response.status_code},{response.text}')
        assert response.status_code == 200, f'Письмо не было получено{response.text}'
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
        response = account_api.put_v1_account_token(new_token)
        assert response.status_code == 200, f'Пользователь был актививирован{response.text}'
        print(f'Повторная активация пользователя {response.status_code},{response.text}')

        # Авторизация пользователя c новым email
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.post_v1_account_login(json_data2)
        print(f'Получение авторизация пользователя {response.status_code},{response.text}')
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'

    def test_unsuccessful_change_email_user(self):
        account_api = AccountApi('http://5.63.153.31:5051')
        login_api = LoginApi('http://5.63.153.31:5051')
        mailhog_api = MailHogApi('http://5.63.153.31:5025')

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
        response = account_api.post_v1_account(json_data1)

        print(f'Создание пользователя {response.status_code},{response.text}')
        assert response.status_code == 201, f'Пользователь не был создан {response.text}'

        # 2 Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(f'Получение письма из почты {response.status_code},{response.text}')
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
        response = account_api.put_v1_account_token(token)
        assert response.status_code == 200, f'Пользователь не был актививирован{response.text}'
        print(f'Активация пользователя {response.status_code},{response.text}')

        # 5 Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.post_v1_account_login(json_data2)
        print(f'Авторизация пользователя {response.status_code},{response.text}')
        assert response.status_code == 200, f'Пользователь не был авторизован{response.text}'

        # 6 смена email
        json_data3 = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = account_api.put_v1_account_email(json_data3)
        assert response.status_code == 400, f'Успешное изменение email на невалидный{response.text}'
        print(f'Смена email {response.status_code},{response.text}')
