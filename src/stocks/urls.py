from django.urls import path
from . import views

app_name = "stocks"

urlpatterns = [
    path("", views.StocksRedirectView.as_view(), name="redirect"),
    path("dashboard/", views.StocksListView.as_view(), name="dashboard"),
    path("<int:pk>/", views.StocksDetailView.as_view(), name="detail"),
    path(
        "add/",
        views.StocksCreateView.as_view(),
        name="add",
    ),
    path(
        "delete/<int:pk>/",
        views.StocksDeleteView.as_view(),
        name="delete",
    ),
]
