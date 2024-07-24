from celery import shared_task
from helpers.stock_watcher import scrape_stock_price
from .models import StockPrice, Stock


@shared_task
def watch_stock_task(ticker: str, exchange: str):
    data = scrape_stock_price(ticker, exchange)

    if not data:
        return None

    StockPrice.objects.create_stock_price(data)


@shared_task
def watch_all_stocks_task():
    qs = Stock.objects.all()
    for obj in qs:
        ticker = obj.ticker
        exchange = obj.exchange
        watch_stock_task.delay(ticker, exchange)
