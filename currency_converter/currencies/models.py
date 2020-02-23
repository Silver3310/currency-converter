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

    def __str__(self) -> str:
        """Short info"""
        return f'{self.base} - {self.target}: {self.rate}'

    class Meta:
        ordering = ['-pk']
        unique_together = [['base', 'target']]
        verbose_name = _('Exchange rate')
        verbose_name_plural = _('Exchange rates')