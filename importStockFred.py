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

def get_filing(statement, stock, count, source, quarterly):
    if quarterly ==1:
        filing = getattr(ob.stocks.fa, statement)(symbol=stock, quarterly=True, limit=count, source=source)
        return filing
    else:
        filing =getattr(ob.stocks.fa, statement)(symbol=stock, limit=count, source=source)
        return filing

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

i_s = 'income'
b_s = 'balance'
cfs = 'cash'

#######################
######Execution########
#######################

##ob.stocks.load(symbol='NVDA', start_date='2018-01-01')

#importing 8 quarterly is for nvda
income_df = get_filing(i_s ,stock, count, source, 0)

#formatting dataframe to convert str to float and dropping B&M
income_df_clean = is_nvda.applymap(convert_to_float)

#importing 8 quarterly bs for nvda
balance_df = get_filing(b_s ,stock, count, source, 1)

#formatting dataframe to convert str to float and dropping B&M
balance_df_clean = bs_nvda.applymap(convert_to_float)

#importing 8 quarterly cfs for nvda
cf_df = get_filing(cfs ,stock, count, source, 1)

#formatting dataframe to convert str to float and dropping B&M
cf_df_clean = cfs_nvda.applymap(convert_to_float)

'''

-Now have quarterly fin filings for NVDA until 08-01-2021

CONSIDER CLASSES

-Next reoder indices to reflect order they appear in filing
-Consider: how will we calculate depreciation, etc. that are found in footnotes in SEC filings??
    -have a function for user to enter that themselves?
        -have functoin to pull up sec filing for them too?
'''

#unformatted filings
print(income_df)
print(balance_df)
print(cf_df)

#formatted filings
print(income_df_clean)
print(balance_df_clean)
print(cf_df_clean)