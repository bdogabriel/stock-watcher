from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone


class Stock(models.Model):
    class Meta:
        verbose_name_plural = "Stocks"
        ordering = ("ticker",)
        constraints = [
            models.UniqueConstraint(
                fields=["ticker", "exchange"], name="stock_ticker_exchange"
            ),
            models.UniqueConstraint(fields=["slug"], name="stock_slug"),
        ]

    ticker = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10)
    slug = models.SlugField()
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

        if not self.id:
            self.slug = slugify(f"{self.ticker} {self.exchange}")

        super().save(*args, **kwargs)


class StockPriceManager(models.Manager):
    def create_stock_price(self, data):
        if not data:
            return None

        stock = Stock.objects.get(slug=data.get("slug"))
        stock.current_price = data.get("current_price")
        stock.save()

        stock_price = self.create(stock=stock, price=stock.current_price)

        return stock_price

    def get_last_half_hour(self, slug):
        stock = Stock.objects.get(slug=slug)
        last_half_hour = datetime.now(tz=get_current_timezone()) - timedelta(minutes=30)
        return self.filter(stock=stock, timestamp__gte=last_half_hour)


class StockPrice(models.Model):
    class Meta:
        verbose_name_plural = "Stock Prices"

    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="stock_prices"
    )
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="BRL")
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = StockPriceManager()

    def __str__(self):
        return f"{self.stock},{self.timestamp},{self.price};"
