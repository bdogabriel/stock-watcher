# from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

# from rest_framework.views import APIView
from .models import Stock
from .serializers import StockSerializer


class StockListCreate(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def delete(self, request, *args, **kwargs):
        Stock.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StockRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    lookup_field = "pk"


# class StockList(APIView):
#     def get(self, request, format=None):
#         ticker = request.query_params.get("ticker", "")

#         if ticker:
#             stock = Stock.objects.filter(ticker__icontains=ticker)
#         else:
#             stock = Stock.objects.all()

#         serializer = StockSerializer(stock, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
