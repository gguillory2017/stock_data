# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 05:24:07 2021

@author: gguil
"""

import json

file = open("SPY.json")
decoder = json.JSONDecoder()
json_obj = decoder.decode(json.load(file))