import pandas as pd

class IBAnalyser():
    
    def executed(self, tickerName, orderId, execPrice, execTotalQty):
        # TO-DO: Looks through currently trading file
        df = pd.read_csv('./database/' + tickerName + '/trades.csv', index_col= 0)
        for index,row in df.iterrows():
            if row['OrderId'] == orderId:
                if row['Quantity'] == execTotalQty:
                    # Parent Order has executed
                    df.loc[index, 'Outcome'] = 'Filled'
                    df.to_csv('./database/' + tickerName + '/trades.csv')
            elif row['OrderId'] + 2 >= orderId:
                if row['Quantity'] == execTotalQty:
                    if row['Position'] == "BUY":
                        if execPrice > row['Entry']:
                            df.loc[index, 'Outcome'] = 'Closed - Profit'
                        elif execPrice < row['Entry']:
                            df.loc[index, 'Outcome'] = 'Closed - Loss'
                        else:
                            df.loc[index, 'Outcome'] = 'Closed - No Change'
                        df.loc[index, 'Profits'] = execPrice - row['Entry'] #TODO Calculate Profit amount ($ x Qty) with leverage
                    elif row['Position'] == "SELL":
                        if execPrice > row['Entry']:
                            df.loc[index, 'Outcome'] = 'Closed - Loss'
                        elif execPrice < row['Entry']:
                            df.loc[index, 'Outcome'] = 'Closed - Profit'
                        else:
                            df.loc[index, 'Outcome'] = 'Closed - No Change'
                        df.loc[index, 'Profits'] = row['Entry'] - execPrice #TODO Calculate Profit amount ($ x Qty) with leverage
                    df.to_csv('./database/' + tickerName + '/trades.csv')
