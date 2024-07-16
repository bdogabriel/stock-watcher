import time
import requests as rq
from babel import numbers as bnums
from bs4 import BeautifulSoup as bs

def currency_str_to_float(str_, currency):
  currency_symbol = bnums.get_currency_symbol(currency)
  return bnums.parse_decimal(str_.strip(currency_symbol))

def get_stock_price(ticker, exchange):
  base_url = "https://www.google.com/finance/quote/"
  response = rq.get(f'{base_url}{ticker}:{exchange}')
  soup = bs(response.text, "html.parser")
  price_div_class = "YMlKec fxKbKc"
  return currency_str_to_float(soup.find(class_=price_div_class).text, 'BRL')

def watch_stock(ticker, exchange, interval):
  while True:
    print(get_stock_price(ticker, exchange))
    time.sleep(interval * 60)