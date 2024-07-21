from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from helpers.class_variables import ClassVariables as Class


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": Class.form_text_input_class,
            }
        ),
    )

    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Your email address",
                "class": Class.form_text_input_class,
            }
        ),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": Class.form_text_input_class,
            }
        ),
    )

    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat your password",
                "class": Class.form_text_input_class,
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
                "class": Class.form_text_input_class,
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": Class.form_text_input_class,
            }
        ),
    )
