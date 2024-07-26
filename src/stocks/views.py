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
from django.utils.text import slugify


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

    def form_valid(self, form):
        ticker = form.data.get("ticker")
        exchange = form.data.get("exchange")
        slug = slugify(f"{ticker} {exchange}")

        stock = Stock.objects.filter(slug=slug)

        if stock:
            print(stock)
            stock.user_add(self.request.user)
            return redirect("stocks:watch", slug=slug)

        return super().form_valid(form)

    def get_success_url(self):
        self.object.user_add(self.request.user)
        self.success_url = reverse_lazy(
            "stocks:watch", kwargs={"slug": self.object.slug}
        )
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
def stock_prices(request, slug):
    if Stock.objects.filter(users=request.user, slug=slug).exists():
        stock_price_serializer = StockPriceSerializer(
            StockPrice.objects.get_last_half_hour(slug), many=True
        )
        return JsonResponse({"prices": stock_price_serializer.data})
    return JsonResponse({"prices": []})


@login_required
def stocks_redirect(request):
    stock = Stock.objects.filter(users=request.user).first()
    if stock is None:
        return redirect("stocks:add")
    return redirect("stocks:watch", slug=stock.slug)
