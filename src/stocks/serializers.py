from rest_framework import serializers
from .models import Stock, StockPrice, UserStockConfig


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = "__all__"


class UserStockConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStockConfig
        fields = "__all__"
