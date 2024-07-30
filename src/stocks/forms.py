from django import forms
from .models import Stock, UserStockConfig

form_text_input_class = "text-gray-700 font-semibold text-center w-16 p-1 rounded-full"
form_select_class = "text-base bg-white text-right mx-auto"


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker", "exchange"]

    ticker = forms.CharField(
        label="Ticker",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ticker",
                "class": f"{form_text_input_class} bg-teal-100",
            }
        ),
        error_messages={"required": "Ticker required!"},
    )

    exchange = forms.CharField(
        label="Exchange",
        initial="BVMF",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Exhange",
                "class": f"{form_text_input_class} bg-cyan-100",
            }
        ),
        error_messages={"required": "Exchange required!"},
    )


class UserStockConfigUpdateForm(forms.ModelForm):
    class Meta:
        model = UserStockConfig
        fields = [
            "tunnel_time_interval",
            "tunnel_range",
            "watch_time_interval",
        ]

    watch_time_interval = forms.ChoiceField(
        label="Watch Interval",
        initial=1,
        choices=[(1, "1 min"), (5, "5 min"), (10, "10 min"), (30, "30 min")],
        widget=forms.Select(
            attrs={
                "class": f"{form_select_class}",
            }
        ),
    )

    tunnel_time_interval = forms.ChoiceField(
        label="Tunnel Interval",
        initial=0,
        choices=[
            (0, "Closing Price"),
            (1, "1 min"),
            (5, "5 min"),
            (10, "10 min"),
            (30, "30 min"),
        ],
        widget=forms.Select(
            attrs={
                "class": f"{form_select_class}",
            }
        ),
    )

    tunnel_range = forms.ChoiceField(
        label="Tunnel Range",
        initial=0.1,
        choices=[(0.1, "10 %"), (0.05, "5 %"), (0.01, "1 %")],
        widget=forms.Select(
            attrs={
                "class": f"{form_select_class} bg-white",
            }
        ),
    )
