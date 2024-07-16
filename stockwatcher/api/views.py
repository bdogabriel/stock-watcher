# from django.shortcuts import render
from rest_framework import generics
from .models import StockPrice
from .serializers import StockPriceSerializer


class StockPriceListCreate(generics.ListCreateAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer
