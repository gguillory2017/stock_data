# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 12:52:13 2021

@author: gguil
"""

from dataclasses import dataclass, field
import typing
from datetime import date
import pandas as pd
from dateutil import relativedelta


frequency_string = '7B'
today = date.today()
one_month= relativedelta.relativedelta(months=+1)
date_range=pd.date_range(today, today + one_month, freq=frequency_string)
dates = date_range.strftime("%Y-%m-%d").tolist()