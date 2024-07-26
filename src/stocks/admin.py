from django.contrib import admin
from .models import Stock, StockPrice, UserStockConfig

# Register your models here.

admin.site.register([Stock, StockPrice, UserStockConfig])
