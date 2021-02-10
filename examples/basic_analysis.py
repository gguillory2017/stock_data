# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 07:34:59 2021

@author: gguil
"""

import json
from datetime import date
from datetime import timedelta
import pandas as pd
import os
import matplotlib.pyplot as plt


# Find todays date and the date 104 weeks ago. Format is yyyy-mm-dd.
current_date = date.today()
num_years = 2
years = timedelta(weeks=52*num_years)
start_date = current_date - years

"""
Find all dates between today and 'num_years' years ago, filter out all days except 
monday, create biweekly list of monday dates
"""

year_range = pd.date_range(start_date, current_date)
all_mondays = list(filter(lambda d: d.dayofweek == 0, year_range))
biweek_mondays = list()
for m in range(len(all_mondays)):
    if m % 2 == 0:
        biweek_mondays.append(str(all_mondays[m].date()))

print(biweek_mondays)

# Load SPY data
data_directory_name = "data_files_"+str(date.today())
data_file = open(data_directory_name+os.path.sep+"SPY.json", "r")
json_decoder = json.JSONDecoder()
json_data_dict = json_decoder.decode(json.load(data_file))

time_stamped_data = json_data_dict["Time Series (Daily)"]

yesterday = current_date - timedelta(days=1)
current_value = float(time_stamped_data[str(yesterday)]["1. open"])

deposit = 200.00
total_investment = 0.0
total_shares = 0.0
complete_data_list = list()
total_investment_values = list()
portfolio_values = list()
total_share_values=list()
for day in biweek_mondays:
    try:
        daily_values = time_stamped_data[day]
    except KeyError:
        print("Could not find data for " + day)
        biweek_mondays.remove(day)
    print(day)
    open_value = float(daily_values['1. open'])
    total_investment += deposit
    total_shares += deposit / open_value
    portfolio_value = total_shares * open_value
    data_dict = {"date": day, "open": open_value, "total investment": total_investment,
                 "total shares": total_shares, "portfolio value": portfolio_value}
    total_investment_values.append(total_investment)
    portfolio_values.append(portfolio_value)
    complete_data_list.append(data_dict)
    total_share_values.append(total_shares)


print("total investment: " + str(total_investment))
print("total shares: " + str(total_shares))
print("value of investment: " + str(total_shares * current_value))
print("profit: " + str((total_shares * current_value) - total_investment))

x=range(len(biweek_mondays))
plt.plot(biweek_mondays, portfolio_values)
plt.plot(biweek_mondays, total_investment_values)
plt.plot(biweek_mondays, total_share_values)
plt.xticks(x,biweek_mondays, rotation='vertical')
