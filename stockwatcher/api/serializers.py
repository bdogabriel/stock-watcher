from rest_framework import serializers
from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",
            "title",
            "ticker",
            "exchange",
            "exchange_title",
            # "timestamp",
            # "price",
        ]
