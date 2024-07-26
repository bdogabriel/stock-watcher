from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import StockPrice, Stock
from .serializers import StockPriceSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from helpers.stock_watcher import get_last_half_hour


@receiver(post_save, sender=StockPrice)
def send_websocket_message(instance, **kwargs):
    stock = instance.stock
    slug = stock.slug

    stock_price_serializer = StockPriceSerializer(
        stock.prices.filter(timestamp__gte=get_last_half_hour()),
        many=True,
    )

    channel_layer = get_channel_layer()

    if channel_layer:
        message = {
            "type": "stock_prices_message",
            "prices": stock_price_serializer.data,
        }
        async_to_sync(channel_layer.group_send)(slug, message)
