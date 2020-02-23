from typing import Union

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from currency_converter.currencies.models import ExchangeRate


class ExchangeRateAPIView(
    APIView
):
    """
    API to calculate exchange rates of the following currencies and a value

    args:
        base (str) - base currency
        target (str) - target currency
        value (float) - the value to convert

    see available currencies in the settings/base.py file (ACTUAL_CURRENCIES)
    """
    def get(self, request, *args, **kwargs):
        base_str: str = self.request.GET.get('base')
        target_str: str = self.request.GET.get('target')
        value: float = float(self.request.GET.get('value', 0.0))
        if not all([base_str, target_str, value]):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'error': 'please specify all the fields!'
                }
            )
        result: Union[None, float] = ExchangeRate.convert_currencies(
            base_str=base_str,
            target_str=target_str,
            value=value
        )  # None if no ExchangeRate for such currencies exists

        if result:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    base_str: value,
                    target_str: result
                }
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'error': 'no data for such currencies'
                }
            )
