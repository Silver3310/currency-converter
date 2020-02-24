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

        from datetime import datetime
        from django_celery_beat.models import CrontabSchedule
        from django_celery_beat.models import PeriodicTask
        from currency_converter.currencies.models import Currency
        from currency_converter.currencies.tasks import update_exchange_rates

        # load exchange rates in case they are not present
        if not Currency.objects.exists():
            update_exchange_rates.delay()

        crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='30',
            hour='12'
        )
        PeriodicTask.objects.get_or_create(
            name='Update exchange rates for the currencies',
            task='currency_converter.currencies.tasks.update_exchange_rates',
            crontab=crontab_schedule,
            description='Update exchange rates for the currencies every day at 12:30 pm UTC',
            start_time=datetime.now()
        )
