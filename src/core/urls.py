from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
]
