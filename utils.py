class Utils():
    @staticmethod
    def get_user_input():
        stock = input("Please enter the stock symbol: ")

        if stock == "Quit" or stock == "quit":
            quit()

        count = input("Please enter the number of filings: ")

        if not count.isdigit() or int(count) <= 0:
            print('Invalid number of filings entered. Please enter a positive integer.\nIf you do not wish to proceed, please type "quit."')
            return get_user_input()

        quarterly = input("Quarterly filings? (Y/N): ")

        if quarterly =='Y' or quarterly == 'y':
            quarterly = 1

        elif quarterly =='N' or quarterly =='n':
            quarterly = 0

        else:
            print('Invalid selection for quarterly data. Please enter Y/N. \nIf you do not wish to proceed, please type "quit."')
            return get_user_input()

        return stock, int(count), quarterly

    @staticmethod
    def order_rename(df, names, order):
        df = df.rename(index=names)
        return df.reindex(order)