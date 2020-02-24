from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate


def load_data_callback(sender, **kwargs):
    """
    Load data at the project startup
    """
    from currency_converter.currencies.models import Currency
    from currency_converter.currencies.tasks import update_exchange_rates

    # load exchange rates in case they are not present
    if not Currency.objects.exists():
        update_exchange_rates.delay()


class CurrenciesConfig(AppConfig):
    name = "currency_converter.currencies"
    verbose_name = _("Currencies")

    def ready(self):
        try:
            import currency_converter.currencies.signals  # noqa F401
        except ImportError:
            pass

        post_migrate.connect(load_data_callback, sender=self)
