from typing import Optional

import pytest

from currency_converter.currencies.models import Currency
from currency_converter.currencies.models import ExchangeRate

pytestmark = pytest.mark.django_db


def test_currency_str():
    currency: Optional[Currency] = Currency.objects.first()
    if currency:
        assert str(currency) == currency.abbr


def test_show_exchange_rates():
    usd_currency: Currency = Currency.objects.get(abbr='USD')
    pln_ex_rate: float = round(ExchangeRate.objects.get(
        base=usd_currency,
        target__abbr='PLN'
    ).rate, 2)
    czk_ex_rate: float = round(ExchangeRate.objects.get(
        base=usd_currency,
        target__abbr='CZK'
    ).rate, 2)
    eur_ex_rate: float = round(ExchangeRate.objects.get(
        base=usd_currency,
        target__abbr='EUR'
    ).rate, 2)
    assert usd_currency.show_exchange_rates() == {
        'PLN': pln_ex_rate,
        'CZK': czk_ex_rate,
        'EUR': eur_ex_rate
    }


def test_exchange_rate_str():
    exchange_rate: Optional[ExchangeRate] = ExchangeRate.objects.first()
    if exchange_rate:
        assert str(exchange_rate) == '{0} - {1}: {2}'.format(
            exchange_rate.base,
            exchange_rate.target,
            exchange_rate.rate
        )


def test_convert_currencies():
    base_str: str = 'USD'
    target_str: str = 'CZK'
    value: float = 21.3
    ex_rate: float = ExchangeRate.objects.get(
        base__abbr=base_str,
        target__abbr=target_str,
    ).rate
    expected_value: float = round(value * ex_rate, 2)

    actual_value = ExchangeRate.convert_currencies(
        base_str=base_str,
        target_str=target_str,
        value=value
    )

    assert expected_value == actual_value
