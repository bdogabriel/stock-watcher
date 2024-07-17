from django.contrib import admin
from .models import Stock, StockPrice

# Register your models here.

admin.site.register([Stock, StockPrice])
