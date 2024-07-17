import requests as rq
from re import sub
from babel import numbers as bnums
from bs4 import BeautifulSoup as bs
from djmoney.money import Money
from django.utils.translation import get_language, to_locale


def currency_str_to_number(str_):
    if not str_:
        return None

    locale = to_locale(get_language())
    value = sub(r"[^\d\-,.]", "", str_)
    return bnums.parse_decimal(value, locale=locale)


def scrape_stock_price(ticker, exchange):
    if not ticker or not exchange:
        return None

    base_url = "https://www.google.com/finance/quote/"
    response = rq.get(f"{base_url}{ticker}:{exchange}")
    soup = bs(response.text, "html.parser")
    price_div_class = "YMlKec fxKbKc"
    title_div_class = "zzDege"
    currency_div_class = "ygUjEc"

    price = currency_str_to_number(soup.find(class_=price_div_class).text)
    title = soup.find(class_=title_div_class).text
    currency = soup.find(class_=currency_div_class).text.split("·")[1].strip()

    if not title:
        title = ""

    if price:
        data = {
            "ticker": ticker,
            "exchange": exchange,
            "title": title,
            "currency": currency,
            "current_price": Money(price, currency),
        }
    else:
        data = None

    return data
