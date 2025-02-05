from contextlib import contextmanager
from requests.exceptions import HTTPError
import requests


@contextmanager
def check_status_kode_http(expected_status_kode: requests.codes = requests.codes.OK,
                           expected_message: str = "",
                           expected_errors_message: str = ""):
    try:
        yield
        if expected_status_kode != requests.codes.OK:
            raise AssertionError(f'Ожидаемый код должен быть равен {expected_status_kode}')
        if expected_message:
            raise AssertionError(f'Должно быть получено сообщение {expected_message}, но запрос прошел успешно')
    except HTTPError as e:
        assert e.response.status_code == expected_status_kode
        assert e.response.json()['title'] == expected_message
        if e.response.json().get('title') == 'Validation failed':
            assert e.response.json().get('errors') == expected_errors_message
