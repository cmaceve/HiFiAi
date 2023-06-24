from openbb_terminal.sdk import openbb as ob
from initFinancials import Data
from constants import Constants

data = Data(Constants.stock, Constants.count, Constants.source)

income_df = data.income_df
income_df



