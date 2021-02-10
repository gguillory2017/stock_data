# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 12:42:43 2021

@author: Alex
"""

import requests as req
import json
import os
import logging
import sys
import time
import datetime
from decouple import config



os.environ['SYMBOL_LIST'] = config('SYMBOL_LIST')
os.environ['TIME_PERIOD'] = config('TIME_PERIOD')
os.environ['API_CALL'] = config('API_CALL')
os.environ['API_KEY'] = config('API_KEY')

logging.basicConfig(filename='data_downloader_log.log', encoding='utf-8', level=logging.DEBUG,
                    filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

if (os.getenv('SYMBOL_LIST') == None):
    logging.error(
        'No symbol list defined. Exiting with status code 1')
    sys.exit(1)

if (os.getenv('TIME_PERIOD') == None):
    logging.warning('No time period provided, setting time period to full')
    os.environ['TIME_PERIOD'] = "full"

if (os.getenv('API_CALL') == None):
    logging.warning(
        'No API call detected for Alpha Vantage API. Using \"TIME_SERIES_DAILY\"')
    os.environ['API_CALL'] = "TIME_SERIES_DAILY"

if (os.getenv('API_KEY') == None):
    logging.error(
        "No Alpha Vantage API key passed. Exiting with exit status code 1.")
    sys.exit(1)

symbol_file_name = os.getenv('SYMBOL_LIST')
symbol_file = open(symbol_file_name, "r")
symbol_list = symbol_file.readlines()
symbol_list = list(map(lambda x: x.strip(), symbol_list))

logging.info("API call being made: " + str(os.getenv('API_CALL')))
logging.info("Time period: " + str(os.getenv('TIME_PERIOD')))
logging.info("Symbols being downloaded: " + str(symbol_list))

data_directory_name = "data_files_"+str(datetime.date.today())

if(not +os.path.exists(data_directory_name)):
    os.mkdir(data_directory_name)

for symbol in symbol_list:
    api_call_string = "https://www.alphavantage.co/query?function=" + \
        str(os.getenv('API_CALL'))+"&symbol=" + \
        symbol+"&outputsize="+str(os.getenv('TIME_PERIOD')) + \
        "&apikey="+str(os.getenv('API_KEY'))
    logging.info("Getting data for symbol: " + symbol)
    api_response = req.get(api_call_string)
    if(api_response.status_code != 200):
        logging.error("Unable to get symbol: " + symbol)
    logging.info("Writing data for symbol: " + symbol)
    output_file = open(data_directory_name+os.path.sep+symbol+".json", "w", encoding='utf-8')
    json.dump(api_response.text, output_file, ensure_ascii=False,indent=0)
    output_file.close()
    logging.info("Wrote data for symbol: " + symbol)
    logging.info("Sleeping for 12 seconds to comply with free tier api rate limit...")
    time.sleep(12)
    
    
logging.info("Finished downloading data for provided symbols.")
sys.exit(0)
