import pytest
from django.urls import reverse, resolve


pytestmark = pytest.mark.django_db


def test_api_exchange_rate_url():
    assert reverse("api:exchange_rate") == "/api/v1/exchange/"
    assert resolve("/api/v1/exchange/").view_name == "api:exchange_rate"


def test_currency_converter_url():
    assert reverse("currencies:home") == "/"
    assert resolve("/").view_name == "currencies:home"
