from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.forms import Form
from django.forms import ModelChoiceField
from django.forms import FloatField

from currency_converter.currencies.models import Currency


class ExchangeRateForm(Form):
    """
    Exchange rate form defining fields the base currency, target currency and
    a value to convert
    """
    base = ModelChoiceField(
        queryset=Currency.objects.filter(abbr__in=settings.ACTUAL_CURRENCIES),
        initial=0,
        required=True,
        label=_('Base currency'),
    )
    target = ModelChoiceField(
        queryset=Currency.objects.filter(abbr__in=settings.ACTUAL_CURRENCIES),
        initial=1,
        required=True,
        label=_('Target currency')
    )
    value = FloatField(
        min_value=0,
        required=True,
        label=_('Value'),
    )

    def clean(self):
        """Check if base and target are different currencies"""
        base = self.cleaned_data.get('base')
        target = self.cleaned_data.get('target')
        if base == target:
            raise ValidationError(
                _('Base and Target currencies have to be different!')
            )
