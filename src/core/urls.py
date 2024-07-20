from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
