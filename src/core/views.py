from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignupForm, LoginForm


class HomeView(TemplateView):
    template_name = "home.html"


class ContactView(TemplateView):
    template_name = "contact.html"


class AboutView(TemplateView):
    template_name = "about.html"


class SignupView(CreateView):
    template_name = "signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("core:login")
    success_message = "Registered!"


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "login.html"
    redirect_authenticated_user = True
