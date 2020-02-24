import requests
from typing import Dict

from django.conf import settings

from config import celery_app

from currency_converter.currencies.models import Currency
from currency_converter.currencies.models import ExchangeRate


@celery_app.task()
def update_exchange_rates() -> None:
    """
    Update the current exchange rates of settings.ACTUAL_CURRENCIES using
    the get_ex_rate_exchanger_source() function
    """

    base_str: str
    for base_str in settings.ACTUAL_CURRENCIES:
        base: Currency
        base, _ = Currency.objects.get_or_create(abbr=base_str)
        targets = [x for x in settings.ACTUAL_CURRENCIES if x != base.abbr]

        current_rates: Dict[str, float] = requests.get(
            settings.EXCHANGE_API_SOURCE,
            params={
                'base': base.abbr,
                'symbols': ','.join(targets)
            }
        ).json()['rates']

        for abbr, rate in current_rates.items():
            target: Currency
            target, _ = Currency.objects.get_or_create(abbr=abbr)
            success: int = ExchangeRate.objects.filter(
                base=base,
                target=target
            ).update(rate=rate)
            if not success:
                ExchangeRate.objects.create(
                    base=base,
                    target=target,
                    rate=rate
                )
