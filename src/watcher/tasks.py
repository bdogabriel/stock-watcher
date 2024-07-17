from celery import shared_task
from helpers.stock_watcher import get_stock_price
from stocks.models import StockPrice, Stock
from stocks.serializers import StockPriceSerializer, StockSerializer


@shared_task
def watch_stock(ticker, exchange):
    data = get_stock_price(ticker, exchange)

    if not data:
        return None

    StockPrice.objects.create_stock_price(data)

    stock_price_serializer = StockPriceSerializer(StockPrice.objects.all(), many=True)
    stock_serializer = StockSerializer(Stock.objects.all(), many=True)
    return (
        f"\nprices: {stock_price_serializer.data}\n\nstocks:{stock_serializer.data}\n"
    )
