import pandas as pd
from openbb_terminal.sdk import openbb as ob
from constants import Constants

class Financials:
    def __init__(self, stock, count, source):
        self.stock = stock
        self.count = count
        self.source = source

    def get_filing(self, statement, quarterly):
        if quarterly==1:
            filing = getattr(ob.stocks.fa, statement)(symbol=self.stock, quarterly=True, limit=self.count, source=self.source)
        else:
            filing = getattr(ob.stocks.fa, statement)(symbol=self.stock, limit=self.count, source=self.source)
        return filing

    @staticmethod
    def convert_to_float(val):
        try:
            if isinstance(val, str):  # check if the value is a string
                if 'B' in val:
                    return float(val.replace('B',''))   # convert billions to millions
                elif 'M' in val:
                    return float(val.replace('M',''))/ 1_000  # keep millions as they are
                elif 'K' in val:
                    return float(val.replace('K',''))/ 1_000_000  # keep millions as they are
                else:
                    return float(val)  # if no 'B' or 'M', just convert to float
        except ValueError:  # handle strings that can't be converted to float
            return val  # if not a string (e.g., NaN values), return as is


