from datetime import datetime

import allure
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to


class GetV1Account:

    @classmethod
    def check_response_value(cls, response):
        with allure.step('Проверка ответа'):
            assert_that(response, all_of(
                has_property('resource', has_property('login', starts_with('aazakharova'))),
                has_property('resource', has_property('registration', instance_of(datetime))),
                has_property('resource', has_properties('rating', has_properties({
                    "enabled": equal_to(True),
                    "quality": equal_to(0),
                    "quantity": equal_to(0)
                }))
                             )))
