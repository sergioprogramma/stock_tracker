STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
KEY = "-"
KEY_NEWS = "-"
account_sid = "-"
auth_token = "-"

import requests
from datetime import date,timedelta
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

today = date.today()
day = date.today().isoweekday()
if day == 1:
    today = (today - timedelta(days=2))
elif day == 7:
    today = (today - timedelta(days=1))

yesterday = f"{today - timedelta(days=1)} 20:00:00"
if day == 2:
    today = (today - timedelta(days=2))

two_days_ago = f"{today - timedelta(days=2)} 20:00:00"

response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK}&interval=60min&apikey={KEY}")
response.raise_for_status()
data = response.json()
first_stock = data["Time Series (60min)"][yesterday]["4. close"]
second_stock = data["Time Series (60min)"][two_days_ago]["4. close"]
difference = (int(float(first_stock)) - int(float(second_stock)))/int(float(second_stock))
difference = round(difference*100, 2)

get_news = False

if difference > 0.05 or difference < -0.05:
    get_news = True

news = requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={today}&sortBy=publishedAt&apiKey={KEY_NEWS}&language=en")
news.raise_for_status()
news_data = news.json()
first_article = news_data["articles"][0]["title"]
second_article = news_data["articles"][2]["title"]
third_article = news_data["articles"][3]["title"]

print(first_article)
print(second_article)
print(third_article)

if difference < 0:
    SMB = "📉"
elif difference > 0:
    SMB = "📈"
else:
    SMB = "😕"


if get_news:
    proxy_client = TwilioHttpClient()

    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"Tesla Inc. in the last business day had a difference of {difference}%{SMB}. And the three main headlines are: \n - {first_article}. \n - {second_article}. \n - {third_article}. \n Have a good day 🚀",
        from_="-",
        to="-"
    )
    print(message.status)
