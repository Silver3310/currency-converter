import pytest

from currency_converter.currencies.forms import ExchangeRateForm

pytestmark = pytest.mark.django_db


class TestExchangeRateForm:
    def test_clean(self):

        # a standard valid form, currencies are from 1 to 4 (choices)
        form = ExchangeRateForm(
            {
                "base": 1,
                "target": 2,
                "value": 123.21,
            }
        )

        assert form.is_valid()

        # a form that has the same currencies
        form = ExchangeRateForm(
            {
                "base": 1,
                "target": 1,
                "value": 123.21,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1

        # value is missing
        form = ExchangeRateForm(
            {
                "base": 1,
                "target": 2,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1

        # value is negative
        form = ExchangeRateForm(
            {
                "base": 1,
                "target": 2,
                "value": -12
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1

        # a form with the same currencies and missing value
        form = ExchangeRateForm(
            {
                "base": 1,
                "target": 1,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 2
