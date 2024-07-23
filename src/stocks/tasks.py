from celery import shared_task
from helpers.stock_watcher import scrape_stock_price
from .serializers import StockPriceSerializer
from .models import StockPrice, Stock
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def watch_stock_task(ticker, exchange):
    data = scrape_stock_price(ticker, exchange)

    if not data:
        return None

    StockPrice.objects.create_stock_price(data)
    stock = Stock.objects.get(ticker=ticker, exchange=exchange)
    stock_price_serializer = StockPriceSerializer(
        StockPrice.objects.filter(stock=stock), many=True
    )

    channel_layer = get_channel_layer()
    if channel_layer:
        message = {
            "type": "stock_prices_message",
            "prices": stock_price_serializer.data,
        }
        async_to_sync(channel_layer.group_send)(f"stock-prices-{stock.pk}", message)

    return stock_price_serializer.data


@shared_task
def watch_all_stocks_task():
    qs = Stock.objects.all()
    for obj in qs:
        ticker = obj.ticker
        exchange = obj.exchange
        watch_stock_task.delay(ticker, exchange)
