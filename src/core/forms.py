from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

form_text_input_class = "w-full py-4 px-6 rounded-xl bg-slate-50"


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": form_text_input_class,
            }
        ),
    )

    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Your email address",
                "class": form_text_input_class,
            }
        ),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": form_text_input_class,
            }
        ),
    )

    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat your password",
                "class": form_text_input_class,
            }
        ),
    )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": form_text_input_class,
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": form_text_input_class,
            }
        ),
    )
