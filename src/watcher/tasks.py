from celery import shared_task
from .stock_watcher import get_stock_price


@shared_task
def watch_stock(ticker, exchange, currency):
    return get_stock_price(ticker, exchange, currency)
