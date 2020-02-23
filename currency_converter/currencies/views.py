from requests import get
from typing import Any

from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import FormView
from django.contrib import messages

from currency_converter.currencies.forms import ExchangeRateForm
from currency_converter.currencies.models import Currency


class CurrencyHomeView(FormView):
    """
    A home page with current exchange rates of currencies and the opportunity
    to convert money between them
    """

    template_name = "pages/home.html"
    form_class = ExchangeRateForm
    success_url = reverse_lazy('currencies:home')

    def form_valid(self, form: ExchangeRateForm):
        base: Currency = form.cleaned_data.get('base')
        target: Currency = form.cleaned_data.get('target')
        value: float = form.cleaned_data.get('value')

        result = get(  # make an API call to our own server
            ''.join([
                'http://',
                self.request.get_host(),
                reverse('api:exchange_rate')]
            ),
            params={
                'base': base.abbr,
                'target': target.abbr,
                'value': str(value)
            }
        ).json()

        messages.add_message(  # show the result as a message
            self.request,
            messages.INFO,
            f'{result[base.abbr]} {base.abbr} => '
            f'{result[target.abbr]} {target.abbr}'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any):
        """Add the currencies to show their current rates"""
        context = super().get_context_data(**kwargs)
        context['currencies'] = Currency.objects.all()
        return context


currency_home_view = CurrencyHomeView.as_view()
