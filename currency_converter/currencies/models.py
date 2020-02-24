from typing import Union
from typing import Dict

from django.db.models import CharField
from django.db.models import FloatField
from django.db.models import ForeignKey

from django.db.models import Model
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _


class Currency(Model):
    """
    Currency that is used for exchange rates

    attrs:
        abbr (str) - abbreviation name of the currency
    """
    abbr = CharField(
        _("Abbreviation name of the currency"),
        max_length=3
    )

    def show_exchange_rates(self) -> Dict[str, float]:
        """Show the rates against this currency and round it to 2"""
        exchange_rates = ExchangeRate.objects.filter(base=self)
        return {
            exchange_rate.target.abbr: round(exchange_rate.rate, 2)
            for exchange_rate in exchange_rates
        }

    def __str__(self) -> str:
        """Return the abbreviation name"""
        return self.abbr

    class Meta:
        ordering = ['-pk']
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


class ExchangeRate(Model):
    """
    Exchange rate for currencies from the Currency model

    attrs:
        base (currency) - base currency
        target (currency) - target currency
        rate (float) - the value of the base currency vs. the target currency
    """
    base = ForeignKey(
        Currency,
        on_delete=CASCADE,
        related_name='base_exchange_rate',
        verbose_name=_("Base currency")
    )
    target = ForeignKey(
        Currency,
        on_delete=CASCADE,
        related_name='target_exchange_rate',
        verbose_name=_("Target currency")
    )
    rate = FloatField(
        _("Exchange rate value")
    )

    @staticmethod
    def convert_currencies(
        base_str: str,
        target_str: str,
        value: float
    ) -> Union[float, None]:
        """
        Convert the money of a given value from the base currency to
        the target currency and round it to 2
        """
        try:
            exchange_rate = ExchangeRate.objects.get(
                base__abbr=base_str,
                target__abbr=target_str,
            )
        except ExchangeRate.DoesNotExist:
            return None
        else:
            return round(exchange_rate.rate * value, 2)

    def __str__(self) -> str:
        """Short info"""
        return f'{self.base} - {self.target}: {self.rate}'

    class Meta:
        ordering = ['-pk']
        unique_together = [['base', 'target']]
        verbose_name = _('Exchange rate')
        verbose_name_plural = _('Exchange rates')
