# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 06:48:19 2021

@author: gguil
"""
from datetime import date
from investment_strategy_class import investment_strategy


s = investment_strategy(14,100.00,2)
print(s.investment_date_set)