######################
#######IMPORTS########
######################

import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import statsmodels.api as sm
from openbb_terminal.sdk import openbb as ob
import re

#######################
######FUNCTIONS########
#######################

def get_is(stock, count, source, quarterly):
    if quarterly ==1:
        statement =ob.stocks.fa.income(symbol=stock, quarterly=True, limit=count, source=source)
        return statement
    else:
        statement =ob.stocks.fa.income(symbol=stock, limit=count, source=source)
        return statement

def get_bs(stock, count, source, quarterly):
    if quarterly ==1:
        statement =ob.stocks.fa.balance(symbol=stock, quarterly=True, limit=count, source=source)
        return statement
    else:
        statement =ob.stocks.fa.balance(symbol=stock, limit=count, source=source)
        return statement
    
def get_cfs(stock, count, source, quarterly):
    if quarterly ==1:
        statement =ob.stocks.fa.cash(symbol=stock, quarterly=True, limit=count, source=source)
        return statement
    else:
        statement =ob.stocks.fa.cash(symbol=stock, limit=count, source=source)
        return statement
    
def convert_to_float(val):
    try:
        if isinstance(val, str):  # check if the value is a string
            if 'B' in val:
                return float(val.replace('B',''))   # convert billions to millions
            elif 'M' in val:
                return float(val.replace('M',''))/ 1_000  # keep millions as they are
            else:
                return float(val)  # if no 'B' or 'M', just convert to float
    except ValueError:  # handle strings that can't be converted to float
        return val  # if not a string (e.g., NaN values), return as is


#######################
######VARIABLES########
#######################

series_ids = {
    'crude_oil_prices': 'DCOILWTICO',
    'cpi': 'CPIAUCSL',
    'unrate': 'UNRATE',
    'ffr': 'FEDFUNDS',
    'mp': 'IPMAN',
    'consumer_sentiment': 'UMCSENT',
    'retail_sales': 'RSAFS',
    'industrial_production': 'INDPRO',
    'housing_starts': 'HOUST',
    'corporate_profits': 'CP',
    'treasury_rate_10y': 'GS10',
    'gdp': 'GDP',
}

start = "2017-01-01"

income = 'income'
stock = 'NVDA'
count = 8
source = 'AlphaVantage'

#######################
######Execution########
#######################

##ob.stocks.load(symbol='NVDA', start_date='2018-01-01')

#importing 8 quarterly is for nvda
is_nvda = get_is(stock, count, source, 1)

#formatting dataframe to convert str to float and dropping B&M
is_nvda_clean = is_nvda.applymap(convert_to_float)
print(is_nvda_clean)

#importing 8 quarterly bs for nvda
bs_nvda = get_bs(stock, count, source, 1)

#formatting dataframe to convert str to float and dropping B&M
bs_nvda_clean = bs_nvda.applymap(convert_to_float)
print(bs_nvda_clean)

#importing 8 quarterly cfs for nvda
cfs_nvda = get_cfs(stock, count, source, 1)

#formatting dataframe to convert str to float and dropping B&M
cfs_nvda_clean = cfs_nvda.applymap(convert_to_float)
print(bs_nvda_clean)
