from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User


class Stock(models.Model):
    class Meta:
        verbose_name_plural = "Stocks"
        ordering = ("ticker",)
        constraints = [
            models.UniqueConstraint(
                fields=["ticker", "exchange"], name="stock_ticker_exchange"
            )
        ]

    ticker = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10)
    title = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    current_price = MoneyField(
        max_digits=19, decimal_places=4, default_currency="BRL", blank=True, null=True
    )
    created_timestamp = models.DateTimeField(auto_now_add=True)
    uptaded_timestamp = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.ticker},{self.exchange},{self.title},{self.currency},{self.current_price},{self.created_timestamp},{self.uptaded_timestamp};"

    def user_delete(self, user):
        self.users.remove(user)
        self.save()

    def user_add(self, user):
        self.users.add(user)
        self.save()

    def save(self, *args, **kwargs):
        self.ticker = self.ticker.upper()
        self.exchange = self.exchange.upper()
        super().save(*args, **kwargs)


class StockPriceManager(models.Manager):
    def create_stock_price(self, data):
        if not data:
            return None

        stock, _ = Stock.objects.update_or_create(data)

        stock_price = self.create(stock=stock, price=data.get("current_price"))

        return stock_price


class StockPrice(models.Model):
    class Meta:
        verbose_name_plural = "Stock Prices"

    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="stock_prices"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="BRL")

    objects = StockPriceManager()

    def __str__(self):
        return f"{self.stock},{self.timestamp},{self.price};"
