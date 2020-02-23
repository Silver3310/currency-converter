from django.urls import path

from currency_converter.currencies.views import currency_home_view


app_name = "currencies"
urlpatterns = [
    path(
        "",
        view=currency_home_view,
        name="home"
    ),
]
