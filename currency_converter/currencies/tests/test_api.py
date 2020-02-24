import pytest
from django.test import RequestFactory
from rest_framework.response import Response

from currency_converter.currencies.models import ExchangeRate
from currency_converter.currencies.api.views import ExchangeRateAPIView

pytestmark = pytest.mark.django_db


class TestExchangeRateAPIView:

    def test_get_success_result(self, request_factory: RequestFactory):
        base_str: str = 'USD'
        target_str: str = 'CZK'
        value: str = '53.2'
        request = request_factory.get(
            "/fake-url/?base={base}&target={target}&value={value}".format(
                base=base_str,
                target=target_str,
                value=value
            )
        )
        view = ExchangeRateAPIView()
        view.request = request
        response: Response = view.get(request)
        result: dict = response.data
        assert response.status_code == 200
        assert type(result) == dict
        assert result[base_str] == float(value)
        expected_result: float = ExchangeRate.convert_currencies(
            base_str=base_str,
            target_str=target_str,
            value=float(value)
        )
        assert result[target_str] == expected_result

    def test_error_something_is_missing(self, request_factory: RequestFactory):
        base_str: str = 'USD'
        value: str = '53.2'
        request = request_factory.get(
            "/fake-url/?base={base}&value={value}".format(
                base=base_str,
                value=value
            )
        )
        view = ExchangeRateAPIView()
        view.request = request
        response: Response = view.get(request)

        assert response.status_code == 400
        assert response.data['error'] == 'please specify all the fields!'

    def test_error_unkown_currency(self, request_factory: RequestFactory):
        base_str: str = 'USD'
        target_str: str = 'QWE'
        value: str = '53.2'
        request = request_factory.get(
            "/fake-url/?base={base}&target={target}&value={value}".format(
                base=base_str,
                target=target_str,
                value=value
            )
        )
        view = ExchangeRateAPIView()
        view.request = request
        response: Response = view.get(request)
        assert response.status_code == 400
        assert response.data['error'] == 'no data for such currencies'
