import pytest
from django.test import RequestFactory
from django.core.management import call_command


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Load fixtures to populate the test DB"""
    with django_db_blocker.unblock():
        call_command('loaddata', 'currencies.currency.json')
        call_command('loaddata', 'currencies.exchangerate.json')
