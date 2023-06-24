from financials import Financials
from utils import Utils
from constants import Constants

class Data:
    def __init__(self, stock, count, source):
        self.financials = Financials(stock, count, source)

        income_data = self.financials.get_filing('income', 1)
        self.income_df = income_data.applymap(self.financials.convert_to_float)
        self.income_df = Utils.order_rename(self.income_df, Constants.rename_dict_is, Constants.order_is)

        balance_data = self.financials.get_filing('balance',1)
        self.balance_df = balance_data.applymap(self.financials.convert_to_float)
        self.balance_df = Utils.order_rename(self.balance_df, Constants.rename_dict_bs, Constants.order_bs)

        cfs_data = self.financials.get_filing('cash',1)
        self.cfs_df = cfs_data.applymap(self.financials.convert_to_float)
        self.cfs_df = Utils.order_rename(self.cfs_df, Constants.rename_dict_cfs, Constants.order_cfs)
