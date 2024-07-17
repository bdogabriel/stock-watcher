from celery import shared_task
from helpers.stock_watcher import get_stock_price
from .serializers import StockPriceSerializer
from django.apps import apps


@shared_task
def watch_stock_task(ticker, exchange):
    data = get_stock_price(ticker, exchange)

    if not data:
        return None

    StockPrice = apps.get_model("stocks", "StockPrice")

    StockPrice.objects.create_stock_price(data)

    stock_price_serializer = StockPriceSerializer(StockPrice.objects.all(), many=True)
    return stock_price_serializer.data
