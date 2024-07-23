from django.urls import path
from . import views

app_name = "stocks"

urlpatterns = [
    path("", views.stocks_redirect, name="dashboard"),
    path("<int:pk>/", views.StocksDetailView.as_view(), name="watch"),
    path("<int:id>/prices/", views.stock_prices, name="prices"),
    path(
        "add/",
        views.StocksCreateView.as_view(),
        name="add",
    ),
    path(
        "delete/<int:pk>/",
        views.StocksDeleteView.as_view(),
        name="delete",
    ),
]
