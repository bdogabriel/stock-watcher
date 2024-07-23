from django.http import JsonResponse
from django.views.generic import View, DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import StockAddForm
from .models import Stock, StockPrice
from .serializers import StockPriceSerializer, StockSerializer
from django.contrib.auth.decorators import login_required


class StocksDashboardMixin(LoginRequiredMixin):
    pass


class StocksView(StocksDashboardMixin, View):  # base view
    template_name = "dashboard.html"
    success_url = reverse_lazy("stocks:dashboard")
    model = Stock
    watch_stock = None

    def get_context_data(self, **kwargs):
        kwargs["stocks_list"] = Stock.objects.filter(users=self.request.user)
        if self.watch_stock:
            stock_serializer = StockSerializer(self.watch_stock)
            kwargs["watch_stock"] = stock_serializer.data
        return super().get_context_data(**kwargs)


class StocksCreateView(StocksView, CreateView):
    form_class = StockAddForm

    def get_context_data(self, **kwargs):
        kwargs["add_stock"] = True
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        stock = Stock.objects.get(
            ticker=form.data.get("ticker"), exchange=form.data.get("exchange")
        )
        if stock:
            stock.user_add(self.request.user)
            return redirect("stocks:dashboard")
        return super().form_invalid(form)

    def get_success_url(self):
        self.object.user_add(self.request.user)
        return super().get_success_url()


class StocksDeleteView(StocksView, DeleteView):
    def form_valid(self, form):
        self.object.user_delete(self.request.user)
        return redirect("stocks:dashboard")

    def get_context_data(self, **kwargs):
        kwargs["delete_stock"] = self.object
        return super().get_context_data(**kwargs)


class StocksDetailView(StocksView, DetailView):
    def get_context_data(self, **kwargs):
        self.watch_stock = self.object
        return super().get_context_data(**kwargs)


@login_required
def stock_prices(request, id):
    stock = Stock.objects.get(users=request.user, id=id)
    stock_price_serializer = StockPriceSerializer(
        StockPrice.objects.filter(stock=stock), many=True
    )
    return JsonResponse({"prices": stock_price_serializer.data})


@login_required
def stocks_redirect(request):
    stock = Stock.objects.filter(users=request.user).first()
    return redirect("stocks:watch", pk=stock.pk)
