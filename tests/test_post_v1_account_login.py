from datetime import datetime

from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to

from chekers.http_chekers import check_status_kode_http


class TestLoginUser:
    def test_successful_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        with check_status_kode_http():
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

    def test_unsuccessful_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login, password, email, with_activate=False)

        with check_status_kode_http(403,'User is inactive. Address the technical support for more details'):
             account_helper.user_login(login, password, validate_headers=False)

