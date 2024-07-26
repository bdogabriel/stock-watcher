from django import forms
from .models import Stock, UserStockConfig
from helpers.class_variables import ClassVariables as Class


class StockAddForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker", "exchange"]

    ticker = forms.CharField(
        label="Ticker",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Stock ticker",
                "class": Class.form_text_input_class,
            }
        ),
    )

    exchange = forms.CharField(
        label="Exchange",
        initial="BVMF",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Stock exhange",
                "class": Class.form_text_input_class,
            }
        ),
    )
