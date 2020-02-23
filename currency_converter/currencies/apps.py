from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CurrenciesConfig(AppConfig):
    name = "currency_converter.currencies"
    verbose_name = _("Currencies")

    def ready(self):
        try:
            import currency_converter.currencies.signals  # noqa F401
        except ImportError:
            pass
