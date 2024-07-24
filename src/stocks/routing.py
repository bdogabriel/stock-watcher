from django.urls import path
from .consumers import DashboardConsumer

websocket_urlpatterns = [
    path("ws/stocks/<slug:slug>/", DashboardConsumer.as_asgi()),
]
