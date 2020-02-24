import requests

import pytest

from currency_converter.currencies.models import Currency
from currency_converter.currencies.models import ExchangeRate
from currency_converter.currencies.tasks import update_exchange_rates

pytestmark = pytest.mark.django_db


class MockResponse:
    """Mock the request.get function"""

    def __init__(self, *args, **kwargs):
        self.base: str = kwargs['params']['base']

    # mock json() method always returns a specific testing dictionary
    def json(self):
        if self.base == 'USD':
            return {
                "rates": {
                    "CZK": 23.2024812517,
                    "EUR": 0.9258402,
                    "PLN": 3.9658364966
                },
                "base": "USD",
                "date": "2020-02-21"
            }
        elif self.base == 'PLN':
            return {
                "rates": {
                    "CZK": 5.8505894712,
                    "EUR": 0.2334539512,
                    "USD": 0.2521536127
                },
                "base": "PLN",
                "date": "2020-02-21"
            }
        elif self.base == 'CZK':
            return {
                "rates": {
                    "EUR": 0.0399026376,
                    "PLN": 0.170922948,
                    "USD": 0.0430988388
                },
                "base": "CZK",
                "date": "2020-02-21"
            }
        elif self.base == 'EUR':
            return {
                "rates": {
                    "CZK": 25.061,
                    "PLN": 4.2835,
                    "USD": 0.123456
                },
                "base": "EUR",
                "date": "2020-02-21"
            }


def test_update_exchange_rates(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse(*args, **kwargs)

    monkeypatch.setattr(requests, "get", mock_get)

    update_exchange_rates()

    # check if our artificial data above was applied
    assert ExchangeRate.objects.get(
        base__abbr='EUR',
        target__abbr='USD',
    ).rate == 0.123456


def test_update_exchange_rates_empty_db(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse(*args, **kwargs)

    monkeypatch.setattr(requests, "get", mock_get)

    # deleting currencies will also delete exchange rates
    Currency.objects.all().delete()

    update_exchange_rates()

    # check if our artificial data above was applied
    assert ExchangeRate.objects.get(
        base__abbr='EUR',
        target__abbr='USD',
    ).rate == 0.123456
