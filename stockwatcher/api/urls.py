from django.urls import path
from . import views

urlpatterns = [
    path(
        "stockprice/",
        views.StockPriceListCreate.as_view(),
        name="stock-price-view-create",
    )
]
