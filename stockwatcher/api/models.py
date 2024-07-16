from django.db import models
from djmoney.models.fields import MoneyField


class Stock(models.Model):
    title = models.CharField(max_length=50)
    ticker = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10)
    exchange_title = models.CharField(max_length=50)
    # timestamp = models.DateTimeField(auto_now_add=True)
    # price = MoneyField(max_digits=19, decimal_places=4, default_currency="BRL")

    def __str__(self):
        return f"{self.ticker},{self.exchange},{self.title},{self.exchange_title};"
