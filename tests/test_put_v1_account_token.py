import random
from json import loads

from api_mailhog.apis.mailhog_api import MailHogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi


class TestActivationUser:

    def test_successful_activation_user(self):
        account_api = AccountApi('http://5.63.153.31:5051')
        login_api = LoginApi('http://5.63.153.31:5051')
        mailhog_api = MailHogApi('http://5.63.153.31:5025')

        random_number = random.randint(1000, 2000)
        login = f'aanastya{random_number}'
        email = f'{login}@mail.ru'
        password = '123456789'

        # Создание пользователя
        json_data1 = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = account_api.post_v1_account(json_data1)

        print(response.status_code)
        assert response.status_code == 201, f'Пользователь не был создан,{response.text}'
        print(response.text)

        # Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(response.status_code)
        assert response.status_code == 200, f'Письмо не было получено{response.text}'
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
        response = account_api.put_v1_account_token(token)
        print(response.status_code)
        print(response.text)

        # Авторизация пользователя
        json_data2 = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = login_api.post_v1_account_login(json_data2)
        print(response.status_code)
        assert response.status_code == 200, f'Пользователь не был авторизован,{response.text}'
        print(response.text)

    def test_unsuccessful_activation_user(self):

        account_api = AccountApi('http://5.63.153.31:5051')
        mailhog_api = MailHogApi('http://5.63.153.31:5025')

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
        response = account_api.post_v1_account(json_data1)

        print(response.status_code)
        assert response.status_code == 201, f'Пользователь не был создан,{response.text}'
        print(response.text)

        # Получение письма из почты
        response = mailhog_api.get_message_from_mail()
        print(response.status_code)
        assert response.status_code == 200, f'Письмо не было получено,{response.text}'
        # resp_js = response.json()

        # Активация пользователя
        token = None
        response = account_api.put_v1_account_token(token)
        assert response.status_code == 400, f'Успешная активация пользователя с пустым токеном,{response.text}'
        print(response.status_code)
        print(response.text)
