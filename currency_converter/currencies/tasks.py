from requests import get
from typing import List, Dict

from django.conf import settings

from config import celery_app

from currency_converter.currencies.models import Currency
from currency_converter.currencies.models import ExchangeRate


def get_exchange_rate_madis_source(
    base: Currency,
    targets: List[str]
) -> Dict[str, float]:
    """
    Update the current exchange rate of the base currency vs the target
    currency from the https://api.exchangeratesapi.io open-source RESTFUL
    service made by Madis Väin
    """
    data = get(settings.EXCHANGE_API_SOURCE.format(
        base=base.abbr,
        targets=','.join(targets)
    ))
    return data.json()['rates']


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
        current_rates: Dict[str, float] = get_exchange_rate_madis_source(
            base=base,
            targets=[x for x in settings.ACTUAL_CURRENCIES if x != base.abbr]
        )
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
