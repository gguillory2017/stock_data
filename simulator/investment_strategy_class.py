# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 12:04:56 2021

@author: gguil
"""


from datetime import date
from datetime import timedelta
import pandas as pd


def calculate_investment_dates(self):
    freqency_string = str(self.reinvestment_period)+'B'
    date_range = pd.date_range(
        start=self.initial_investment_date, end=date.today(), freq=freqency_string)
    #change to set
    return list(map(lambda d : d.date(), date_range))
            
def calculate_initial_investment_date(self):
    number_of_weeks = timedelta(weeks=(52*self.total_investment_period))
    return date.today() - number_of_weeks


class investment_strategy:
        def __init__(self, period, deposit, time):
            self.reinvestment_period = period
            self.reoccuring_deposit_amount = deposit
            self.total_investment_period = time
            self.initial_investment_date = calculate_initial_investment_date(self)
            self.investment_date_set =calculate_investment_dates(self)
            


