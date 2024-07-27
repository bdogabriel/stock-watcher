from django import forms
from .models import Stock

form_text_input_class = (
    "text-gray-700 font-semibold text-center w-16 py-1 px-1 rounded-full"
)


class StockAddForm(forms.ModelForm):
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
