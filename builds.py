from openbb_terminal.sdk import openbb as ob
from initFinancials import Data
from constants import Constants

data = Data(Constants.stock, Constants.count, Constants.source)

income_df = data.income_df

'''
Begin building income projections. Think of breaking down unit cost/other industry standard measurements
i.e., productivity space, customer traffic etc.
'''
