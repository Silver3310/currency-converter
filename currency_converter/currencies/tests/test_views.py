import requests

import pytest
from django.test import RequestFactory
from django.contrib import messages

from currency_converter.currencies.forms import ExchangeRateForm
from currency_converter.currencies.views import CurrencyHomeView

pytestmark = pytest.mark.django_db


class MockResponse:
    """Mock the request.get function"""

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {
            'USD': '23.2',
            'EUR': '21.43'
        }


class TestCurrencyHomeView:
    def test_get_success_url(self, request_factory: RequestFactory):
        view = CurrencyHomeView()
        request = request_factory.get("/fake-url/")

        view.request = request

        assert view.get_success_url() == "/"

    def test_form_valid(self, request_factory: RequestFactory, monkeypatch):
        view = CurrencyHomeView()
        request = request_factory.get("/fake-url/")

        def mock_get(*args, **kwargs):
            return MockResponse()

        # messages are not needed for the tests
        def mock_add_message(*args, **kwargs):
            pass

        monkeypatch.setattr(requests, "get", mock_get)
        monkeypatch.setattr(messages, 'add_message', mock_add_message)

        view.request = request
        form = ExchangeRateForm(
            {
                'base': 1,
                'target': 3,
                'value': 23.2
            }
        )
        form.is_valid()

        assert view.form_valid(form)

    def test_context_data(self, request_factory: RequestFactory):
        view = CurrencyHomeView()
        request = request_factory.get("/fake-url/")

        view.request = request

        assert 'currencies' in view.get_context_data()
