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

def order_rename(df, names, order):
    df = df.rename(index=names)

    return df.reindex(order)

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

order_is = [
    'Reported Currency',
    'Total Revenue',
    'Cost of Goods and Services Sold',
    'Gross Profit',
    'Selling, General and Administrative',
    'Research and Development',
    'Operating Expenses',
    'Operating Income',
    'Interest Income',
    'Interest Expense',
    'Interest and Debt Expense',
    'Net Interest Income',
    'Investment Income (Net)',
    'Non-Interest Income',
    'Other Non-Operating Income',
    'Income Before Tax',
    'Income Tax Expense',
    'Net Income',
    'Depreciation and Amortization',
    'EBITDA'
]


rename_dict_is = {
    'fiscalDateEnding': 'Fiscal Date Ending',
    'reportedCurrency': 'Reported Currency',
    'grossProfit': 'Gross Profit',
    'totalRevenue': 'Total Revenue',
    'costOfRevenue': 'Cost of Revenue',
    'costofGoodsAndServicesSold': 'Cost of Goods and Services Sold',
    'operatingIncome': 'Operating Income',
    'sellingGeneralAndAdministrative': 'Selling, General and Administrative',
    'researchAndDevelopment': 'Research and Development',
    'operatingExpenses': 'Operating Expenses',
    'investmentIncomeNet': 'Investment Income (Net)',
    'netInterestIncome': 'Net Interest Income',
    'interestIncome': 'Interest Income',
    'interestExpense': 'Interest Expense',
    'nonInterestIncome': 'Non-Interest Income',
    'otherNonOperatingIncome': 'Other Non-Operating Income',
    'depreciationAndAmortization': 'Depreciation and Amortization',
    'incomeBeforeTax': 'Income Before Tax',
    'incomeTaxExpense': 'Income Tax Expense',
    'interestAndDebtExpense': 'Interest and Debt Expense',
    'ebitda': 'EBITDA',
    'netIncome': 'Net Income'
}

order_bs = [
    'Reported Currency',
    'Total Current Assets',
    'Cash And Cash Equivalents At Carrying Value',
    'Cash And Short Term Investments',
    'Inventory',
    'Current Net Receivables',
    'Other Current Assets',
    'Total Non-Current Assets',
    'PPE',
    'Accumulated Depreciation Amortization PPE',
    'Intangible Assets',
    'Intangible Assets Excluding Goodwill',
    'Goodwill',
    'Investments',
    'Long Term Investments',
    'Short Term Investments',
    'Other Non Current Assets',
    'Total Assets',
    'Total Current Liabilities',
    'Current Accounts Payable',
    'Deferred Revenue',
    'Current Debt',
    'Short Term Debt',
    'Other Current Liabilities',
    'Total Non-Current Liabilities',
    'Capital Lease Obligations',
    'Long Term Debt',
    'Current Long Term Debt',
    'Long Term Debt Noncurrent',
    'Short Long Term Debt Total',
    'Other Non-Current Liabilities',
    'Total Liabilities',
    'Shareholder Equity',
    'Common Stock',
    'Treasury Stock',
    'Earnings',
    'Common Stock Shares Outstanding'
]

rename_dict_bs = {
 'reportedCurrency': 'Reported Currency', 'totalAssets': 'Total Assets',
 'totalCurrentAssets': 'Total Current Assets', 'cashAndCashEquivalentsAtCarryingValue': 'Cash And Cash Equivalents At Carrying Value',
 'cashAndShortTermInvestments': 'Cash And Short Term Investments', 'inventory': 'Inventory', 'currentNetReceivables': 'Current Net Receivables',
 'totalNonCurrentAssets': 'Total Non-Current Assets', 'propertyPlantEquipment': 'PPE',
 'accumulatedDepreciationAmortizationPPE': 'Accumulated Depreciation Amortization PPE', 'intangibleAssets': 'Intangible Assets',
 'intangibleAssetsExcludingGoodwill': 'Intangible Assets Excluding Goodwill', 'goodwill': 'Goodwill', 'investments': 'Investments',
 'longTermInvestments': 'Long Term Investments', 'shortTermInvestments': 'Short Term Investments', 'otherCurrentAssets': 'Other Current Assets',
 'otherNonCurrentAssets': 'Other Non Current Assets', 'totalLiabilities': 'Total Liabilities', 'totalCurrentLiabilities': 'Total Current Liabilities',
 'currentAccountsPayable': 'Current Accounts Payable', 'deferredRevenue': 'Deferred Revenue', 'currentDebt': 'Current Debt',
 'shortTermDebt': 'Short Term Debt', 'totalNonCurrentLiabilities': 'Total Non-Current Liabilities', 'capitalLeaseObligations': 'Capital Lease Obligations',
 'longTermDebt': 'Long Term Debt', 'currentLongTermDebt': 'Current Long Term Debt', 'longTermDebtNoncurrent': 'Long Term Debt Noncurrent',
 'shortLongTermDebtTotal': 'Short Long Term Debt Total', 'otherCurrentLiabilities': 'Other Current Liabilities',
 'otherNonCurrentLiabilities': 'Other Non-Current Liabilities', 'totalShareholderEquity': 'Shareholder Equity', 'treasuryStock': 'Treasury Stock',
 'retainedEarnings': 'Earnings', 'commonStock': 'Common Stock', 'commonStockSharesOutstanding': 'Common Stock Shares Outstanding'
}


rename_dict_cfs = {
    'reportedCurrency': 'Reported Currency',
    'operatingCashflow': 'Operating Cashflow',
    'paymentsForOperatingActivities': 'Payments For Operating Activities',
    'proceedsFromOperatingActivities': 'Proceeds From Operating Activities',
    'changeInOperatingLiabilities': 'Change In Operating Liabilities',
    'changeInOperatingAssets': 'Change In Operating Assets',
    'depreciationDepletionAndAmortization': 'Depreciation Depletion And Amortization',
    'capitalExpenditures': 'Capital Expenditures',
    'changeInReceivables': 'Change In Receivables',
    'changeInInventory': 'Change In Inventory',
    'profitLoss': 'Profit Loss',
    'cashflowFromInvestment': 'Cashflow From Investment',
    'cashflowFromFinancing': 'Cashflow From Financing',
    'proceedsFromRepaymentsOfShortTermDebt': 'Proceeds From Repayments Of Short Term Debt',
    'paymentsForRepurchaseOfCommonStock': 'Payments For Repurchase Of Common Stock',
    'paymentsForRepurchaseOfEquity': 'Payments For Repurchase Of Equity',
    'paymentsForRepurchaseOfPreferredStock': 'Payments For Repurchase Of Preferred Stock',
    'dividendPayout': 'Dividend Payout',
    'dividendPayoutCommonStock': 'Dividend Payout Common Stock',
    'dividendPayoutPreferredStock': 'Dividend Payout Preferred Stock',
    'proceedsFromIssuanceOfCommonStock': 'Proceeds From Issuance Of Common Stock',
    'proceedsFromIssuanceOfLongTermDebtAndCapitalSecurities': 'Proceeds From Issuance Of Long Term Debt And Capital Securities',
    'proceedsFromIssuanceOfPreferredStock': 'Proceeds From Issuance Of Preferred Stock',
    'proceedsFromRepurchaseOfEquity': 'Proceeds From Repurchase Of Equity',
    'proceedsFromSaleOfTreasuryStock': 'Proceeds From Sale Of Treasury Stock',
    'changeInCashAndCashEquivalents': 'Change In Cash And Cash Equivalents',
    'changeInExchangeRate': 'Change In Exchange Rate',
    'netIncome': 'Net Income'
}

order_cfs = [
    'Reported Currency',
    'Operating Cashflow',
    'Depreciation Depletion And Amortization',
    'Change In Operating Assets',
    'Change In Operating Liabilities',
    'Payments For Operating Activities',
    'Proceeds From Operating Activities',
    'Change In Receivables',
    'Change In Inventory',
    'Profit Loss',
    'Cashflow From Investment',
    'Capital Expenditures',
    'Cashflow From Financing',
    'Payments For Repurchase Of Common Stock',
    'Payments For Repurchase Of Equity',
    'Payments For Repurchase Of Preferred Stock',
    'Proceeds From Repayments Of Short Term Debt',
    'Dividend Payout',
    'Dividend Payout Common Stock',
    'Dividend Payout Preferred Stock',
    'Proceeds From Issuance Of Common Stock',
    'Proceeds From Issuance Of Long Term Debt And Capital Securities',
    'Proceeds From Issuance Of Preferred Stock',
    'Proceeds From Repurchase Of Equity',
    'Proceeds From Sale Of Treasury Stock',
    'Change In Cash And Cash Equivalents',
    'Change In Exchange Rate',
    'Net Income'
]

#######################
######Execution########
#######################

##ob.stocks.load(symbol='NVDA', start_date='2018-01-01')

#importing 8 quarterly is for nvda
income_df = get_filing(i_s ,stock, count, source, 1)

#formatting dataframe to convert str to float and dropping B&M
income_df = income_df.applymap(convert_to_float)

#importing 8 quarterly bs for nvda
balance_df = get_filing(b_s ,stock, count, source, 1)

#formatting dataframe to convert str to float and dropping B&M
balance_df = balance_df.applymap(convert_to_float)

#importing 8 quarterly cfs for nvda
cfs_df = get_filing(cfs ,stock, count, source, 1)

#formatting dataframe to convert str to float and dropping B&M
cfs_df = cfs_df.applymap(convert_to_float)

'''

-Now have quarterly fin filings for NVDA until 08-01-2021

CONSIDER CLASSES

-Consider: how will we calculate depreciation, etc. that are found in footnotes in SEC filings??
    -have a function for user to enter that themselves?
        -have functoin to pull up sec filing for them too?
'''

income_df = income_df.drop(['comprehensiveIncomeNetOfTax', 'ebit', 'depreciation'])
income_df_final = order_rename(income_df, rename_dict_is, order_is)

balance_df_final = order_rename(balance_df, rename_dict_bs, order_bs)

cfs_df_final = order_rename(cfs_df, rename_dict_cfs, order_cfs)
cfs_df_final.drop(['Proceeds From Issuance Of Long Term Debt And Capital Securities'], inplace = True)


print(income_df_final)
print(balance_df_final)
print(cfs_df_final)