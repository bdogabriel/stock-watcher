from django.urls import path
from .consumers import DashboardConsumer

websocket_urlpatterns = [
    path("ws/stocks/<int:pk>/", DashboardConsumer.as_asgi()),
]
