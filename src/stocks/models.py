from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.utils.text import slugify


class Stock(models.Model):
    class Meta:
        verbose_name = "Stock"
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
    slug = models.SlugField(default="")
    title = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    current_price = MoneyField(
        max_digits=19, decimal_places=4, default_currency="BRL", blank=True, null=True
    )
    last_closing_price = MoneyField(
        max_digits=19, decimal_places=4, default_currency="BRL", blank=True, null=True
    )
    created_timestamp = models.DateTimeField(auto_now_add=True)
    uptaded_timestamp = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name="users")

    def __str__(self):
        return f"{self.ticker},{self.exchange},{self.slug},{self.title},{self.currency},{self.current_price},{self.created_timestamp},{self.uptaded_timestamp};"

    def user_delete(self, user):
        self.users.remove(user)
        UserStockConfig.objects.get(user=user, stock=self).delete()
        self.save()

    def user_add(self, user):
        self.users.add(user)
        config = UserStockConfig.objects.create(user=user, stock=self)
        config.save()
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

        stock, _ = Stock.objects.update_or_create(
            slug=data.get("slug"),
            ticker=data.get("ticker"),
            exchange=data.get("exchange"),
            defaults=data,
        )

        stock_price = self.create(stock=stock, price=stock.current_price)

        return stock_price


class StockPrice(models.Model):
    class Meta:
        verbose_name = "Stock Price"
        verbose_name_plural = "Stock Prices"
        ordering = ("timestamp",)

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="prices")
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="BRL")
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = StockPriceManager()

    def __str__(self):
        return f"{self.stock.slug},{self.timestamp},{self.price};"


class UserStockConfig(models.Model):
    class Meta:
        verbose_name = "User Stock Config"
        verbose_name_plural = "User Stock Configs"
        constraints = [
            models.UniqueConstraint(fields=["user", "stock"], name="config_user_stock"),
        ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stocks_configs"
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="users_configs",
        default="",
    )
    watch_time_interval = models.IntegerField(
        default=1
    )  # time interval to get stock price

    # time interval to update tunnel value
    # 0: tunnel will be fixed on the last closing value
    tunnel_time_interval = models.IntegerField(default=0)

    # value multiplied by the price to get tunnel value
    tunnel_range = models.FloatField(default=0.1)

    def __str__(self):
        return f"{self.user},{self.stock.slug},{self.watch_time_interval},{self.tunnel_time_interval},{self.tunnel_range};"
