from django.urls import path
from . import views

app_name = "stocks"

urlpatterns = [
    path("", views.StocksRedirectView.as_view(), name="dashboard"),
    path(
        "add/",
        views.StocksCreateView.as_view(),
        name="add",
    ),
    path("<slug:slug>/", views.StocksDetailView.as_view(), name="watch"),
    path(
        "<slug:slug>/add/",
        views.StocksCreateView.as_view(),
        name="add",
    ),
    path(
        "<slug:slug>/config/",
        views.UserStockConfigUpdateView.as_view(),
        name="config",
    ),
    path("<slug:slug>/prices/", views.stock_prices, name="prices"),
    path(
        "<slug:slug>/delete/",
        views.StocksDeleteView.as_view(),
        name="delete",
    ),
]
