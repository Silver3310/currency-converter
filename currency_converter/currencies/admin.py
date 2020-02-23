from django.contrib.admin import register
from django.contrib.admin import ModelAdmin

from currency_converter.currencies.models import Currency
from currency_converter.currencies.models import ExchangeRate


@register(Currency)
class CurrencyAdmin(ModelAdmin):
    """
    Admin panel for the Currency model
    """

    list_display = ["pk", "abbr"]
    search_fields = ["abbr"]


@register(ExchangeRate)
class ExchangeRateAdmin(ModelAdmin):
    """
    Admin panel for the ExchangeRate model
    """

    list_display = ["base", "target", "rate"]
    search_fields = ["base", "target"]
