from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.views.generic import View, DetailView, RedirectView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .forms import StockCreateForm, UserStockConfigUpdateForm
from .models import Stock, UserStockConfig
from .serializers import (
    StockPriceSerializer,
    StockSerializer,
    UserStockConfigSerializer,
)
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from helpers.stock_watcher import get_last_half_hour


class StocksDashboardMixin(LoginRequiredMixin):
    pass


class BaseView(StocksDashboardMixin, View):
    template_name = "dashboard.html"
    success_url = reverse_lazy("stocks:dashboard")

    def get_context_data(self, **kwargs):
        kwargs["stocks_list"] = Stock.objects.filter(users=self.request.user)
        if "watch_stock" in kwargs:
            stock = kwargs["watch_stock"]

            stock_serializer = StockSerializer(stock)
            config_serializer = UserStockConfigSerializer(
                stock.users_configs.filter(user=self.request.user), many=True
            )

            kwargs["watch_stock"] = stock_serializer.data
            kwargs["watch_stock_config"] = config_serializer.data
        return super().get_context_data(**kwargs)


class StocksView(BaseView):
    model = Stock


class UserStocksConfigView(BaseView):
    model = UserStockConfig


class UserStockConfigUpdateView(UserStocksConfigView, UpdateView):
    form_class = UserStockConfigUpdateForm

    def get_object(self, _=None):
        return UserStockConfig.objects.get(
            user=self.request.user, stock=Stock.objects.get(slug=self.kwargs["slug"])
        )

    def get_context_data(self, **kwargs):
        kwargs["update_user_stock_config"] = True
        kwargs["watch_stock"] = self.object.stock
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        self.success_url = reverse(
            "stocks:watch", kwargs={"slug": self.object.stock.slug}
        )
        return super().get_success_url()


class StocksCreateView(StocksView, CreateView):
    form_class = StockCreateForm

    def get_context_data(self, **kwargs):
        kwargs["create_stock"] = True
        if "slug" in self.kwargs:
            kwargs["watch_stock"] = Stock.objects.get(slug=self.kwargs["slug"])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        ticker = form.data.get("ticker")
        exchange = form.data.get("exchange")
        slug = slugify(f"{ticker} {exchange}")

        if Stock.objects.filter(slug=slug).exists():
            stock = Stock.objects.get(slug=slug)
            stock.user_add(self.request.user)
            return redirect("stocks:watch", slug=slug)

        return super().form_valid(form)

    def get_success_url(self):
        self.object.user_add(self.request.user)
        self.success_url = reverse("stocks:watch", kwargs={"slug": self.object.slug})
        return super().get_success_url()


class StocksDeleteView(StocksView, DeleteView):
    def form_valid(self, form):
        self.object.user_delete(self.request.user)
        return redirect("stocks:dashboard")

    def get_context_data(self, **kwargs):
        kwargs["delete_stock"] = self.object
        kwargs["watch_stock"] = self.object
        return super().get_context_data(**kwargs)


class StocksDetailView(StocksView, DetailView):
    def get_context_data(self, **kwargs):
        kwargs["watch_stock"] = self.object
        return super().get_context_data(**kwargs)


class StocksRedirectView(StocksDashboardMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        stock = Stock.objects.filter(users=self.request.user).first()
        if stock is None:
            self.pattern_name = "stocks:add"
        else:
            self.pattern_name = "stocks:watch"
            kwargs["slug"] = stock.slug
        return super().get_redirect_url(*args, **kwargs)


@login_required
def stock_prices(request, slug):
    if Stock.objects.filter(users=request.user, slug=slug).exists():
        stock = Stock.objects.get(users=request.user, slug=slug)
        stock_price_serializer = StockPriceSerializer(
            stock.prices.filter(timestamp__gte=get_last_half_hour()),
            many=True,
        )
        return JsonResponse({"prices": stock_price_serializer.data})
    return JsonResponse({"prices": []})
