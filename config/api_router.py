from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings
from django.urls import path

from currency_converter.currencies.api.views import ExchangeRateAPIView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


api_view_routes = [
    path(
        'exchange/',
        ExchangeRateAPIView.as_view(),
        name='api_exchange_rate'
    ),
]


app_name = "api"
urlpatterns = router.urls + api_view_routes
