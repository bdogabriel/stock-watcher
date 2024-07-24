from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import StockPrice
from .serializers import StockPriceSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=StockPrice)
def send_websocket_message(instance, **kwargs):
    slug = instance.stock.slug

    stock_price_serializer = StockPriceSerializer(
        StockPrice.objects.get_last_half_hour(slug),
        many=True,
    )

    channel_layer = get_channel_layer()

    if channel_layer:
        message = {
            "type": "stock_prices_message",
            "prices": stock_price_serializer.data,
        }
        async_to_sync(channel_layer.group_send)(slug, message)
