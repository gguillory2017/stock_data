# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 12:42:43 2021

@author: Alex
"""

import requests as req 
import json 
import sys
from datetime import date
from datetime import timedelta
import pandas as pd
import time

#Constants. Stock symbol and default Polygon.io api key

symbol = "SPY"
api_key = "uYz7sNo_YtPlGbpvtERsv356PmRw5_gY"

#Find todays date and the date 104 weeks ago. Format is yyyy-mm-dd.

current_date = date.today()
two_years=timedelta(weeks=52*2)
start_date=current_date - two_years

print("Gathering stock price information for symbol " + symbol + " for dates: " + str(start_date) + " - " + str(current_date))


"""
Find all dates between today and 2 years ago, filter out all days except 
monday, create biweekly list of monday dates
"""

two_year_range = pd.date_range(start_date, current_date)
all_mondays = list(filter(lambda d : d.dayofweek == 0, two_year_range))
biweek_mondays=list()
for m in range(len(all_mondays)):
    if m % 2 == 0:
        biweek_mondays.append(all_mondays[m])

#Begin collecting data, sleeping every 20 seconds to comply with api rate limits

stock_price_json_responses = list()
stock_price_external_file = open("spy_prices.txt", "a")

for d in biweek_mondays:
    daily_oc_request="https://api.polygon.io/v1/open-close/"+symbol+"/"+str(d.date())+"?unadjusted=true&apiKey="+api_key
    print("Getting stock price information for: " + symbol + " on day: " + str(d.date()))
    daily_oc_response=req.get(daily_oc_request)
    daily_oc_json=json.loads(daily_oc_response.content)
    if (daily_oc_response.status_code != 200):
        print("HTTP response not 200 - could not get price for symbol: " + symbol + " on day: " + str(d.date()))
    print("Successfully retrieved price of: " + symbol + " on day: " + str(d.date()))
    stock_price_json_responses.append(daily_oc_json)
    print("Writing to external file")
    stock_price_external_file.write(str(daily_oc_json)+'\n')
    print("sleeping...")
    time.sleep(12)

stock_price_external_file.close()
print("closed external file and exiting...")
