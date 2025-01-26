from datetime import datetime

from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to


class TestLoginUser:
    def test_successful_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login, password, email)
        response = account_helper.user_login(login, password, validate_response=True)
        assert_that(response, all_of(
            has_property('resource', has_property('login', starts_with('aanastya'))),
            has_property('resource', has_property('registration', instance_of(datetime))),
            has_property('resource', has_properties('rating', has_properties({
                "enabled": equal_to(True),
                "quality": equal_to(0),
                "quantity": equal_to(0)
            }))
                         )))

        print(response)

    def test_unsuccessful_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        response = account_helper.register_new_user(login, password, email, with_activate=False)
        assert response.status_code == 201, f'Пользователь не был создан{response.text}'

        response = account_helper.user_login(login, password, validate_headers=False)
        assert response.status_code == 403, f'Пользователь был авторизован без активации{response.text}'
