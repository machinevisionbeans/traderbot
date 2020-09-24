import Pyro4
import pandas as pd

class Comparator():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.executor = Pyro4.Proxy("PYRONAME:executor")

    def updateWeightage(self, strategy, points):
        df = pd.read_csv('./database/' + self.tickerName + '/IndicatorScore.csv', index_col=0)

        if points < 0:
            df.loc[0, strategy] = 0.9 * df.loc[0, strategy]
            # fibonacci increment strategy
            # if df.loc[2,strategy] > 0:
            #     df.loc[2,strategy] = -1
            #     df.loc[1,strategy] = 0
            # else:
            #     temp = df.loc[2,strategy]
            #     df.loc[2,strategy] = df.loc[2,strategy] + df.loc[1,strategy]
            #     df.loc[1,strategy] = temp
        else:
            df.loc[0, strategy] = 1.1 * df.loc[0,strategy]
            # fibonacci decrement strategy
            # if df.loc[2,strategy] < 0:
            #     df.loc[2,strategy] = 1
            #     df.loc[1,strategy] = 0
            # else:
            #     temp = df.loc[2, strategy]
            #     df.loc[2,strategy] = df.loc[2,strategy] + df.loc[1,strategy]
            #     df.loc[1,strategy] = temp

        # fibonacci strategy
        # df.loc[0,strategy] = df.loc[0,strategy] + df.loc[2,strategy]
        df.to_csv('./database/' + self.tickerName + '/IndicatorScore.csv')
        pass
    
    def compare(self, results, timestamp):
        # TO-DO: Compare results and output final decision
        df = pd.read_csv('./database/' + self.tickerName + '/IndicatorScore.csv', index_col=0)

        # 1. Get the weightage
        init = False

        for i in results:
            if init == False:
                highest = df.loc[0,i] * (results[i])["position"]
                lowest = df.loc[0,i] * (results[i])["position"]
                highestIndicator = i
                lowestIndicator = i
                init = True
            else:
                if df.loc[0,i] * (results[i])["position"] > highest:
                    highest = df.loc[0,i] * (results[i])["position"]
                    highestIndicator = i
                if df.loc[0,i] * (results[i])["position"] < lowest:
                    lowest = df.loc[0,i] * (results[i])["position"]
                    lowestIndicator = i
            
            df.loc[0,i] = df.loc[0,i] * (results[i])["position"]

        total = df.sum(axis = 1)

        if total[0] > 100:
            if total[0] > 500: leverage = 5
            elif total[0] > 200: leverage = 2
            else: leverage = 1
            tradeWindow = pd.read_csv('./database/' + self.tickerName + '/trades.csv', index_col= 0)
            tradeWindow = tradeWindow.append({'Time Stamp' : timestamp, 'Position': 1, 'Amount': results[highestIndicator]["amount"], 'Entry': results[highestIndicator]["entry"], 'Stop Loss': results[highestIndicator]["stoploss"], 'Target': results[highestIndicator]["takeprofit"], 'Leverage': leverage, 'Outcome': 'Pending', 'Profits': 0}, ignore_index = True)
            tradeWindow.to_csv('./database/' + self.tickerName + '/trades.csv')
            self.executor.execute(self.tickerName, 1, results[highestIndicator]["amount"], results[highestIndicator]["stoploss"], results[highestIndicator]["takeprofit"], leverage)
        elif total[0] < -100:
            if total[0] < -500: leverage = 5
            elif total[0] < -200: leverage = 2
            else: leverage = 1
            tradeWindow = pd.read_csv('./database/' + self.tickerName + '/trades.csv', index_col= 0)
            tradeWindow = tradeWindow.append({'Time Stamp' : timestamp, 'Position': -1, 'Amount': results[lowestIndicator]["amount"], 'Entry': results[lowestIndicator]["entry"], 'Stop Loss': results[lowestIndicator]["stoploss"], 'Target': results[lowestIndicator]["takeprofit"], 'Leverage': leverage, 'Outcome': 'Pending', 'Profits': 0}, ignore_index = True)
            tradeWindow.to_csv('./database/' + self.tickerName + '/trades.csv')
            self.executor.execute(self.tickerName, -1, results[lowestIndicator]["amount"], results[lowestIndicator]["stoploss"], results[lowestIndicator]["takeprofit"], leverage)
        pass

    def intervalAnalysis(self, update):
        df = pd.read_csv('./database/' + self.tickerName + '/trades.csv', index_col= 0)
        for index,row in df.iterrows():
            if row['Outcome'] == 'Pending':
                if row['Position'] == 1:
                    if update['high'].values[0] > row['Target']:
                        oldPriceDifference = row['Target'] - row['Entry']
                        newPriceDifference = 1.5 * oldPriceDifference
                        df.loc[index, 'Stop Loss'] = row['Target']
                        df.loc[index, 'Target'] = row['Entry'] + newPriceDifference
                        df.loc[index, 'Profits'] = (update['close'].values[0] - df.loc[index, 'Entry']) / df.loc[index,'Entry'] * df.loc[index, 'Amount'] * df.loc[index, 'Leverage']
                        df.to_csv('./database/' + self.tickerName + '/trades.csv')

                    elif update['low'].values[0] < row['Stop Loss']:
                        df.loc[index, 'Outcome'] = 'Closed'
                        df.loc[index, 'Profits'] = (df.loc[index,'Stop Loss'] - df.loc[index,'Entry']) / df.loc[index,'Entry'] * df.loc[index,'Amount'] * df.loc[index, 'Leverage']
                        df.to_csv('./database/' + self.tickerName + '/trades.csv')

                elif row['Position'] == -1:
                    if update['low'].values[0] < row['Target']:
                        oldPriceDifference = row['Entry'] - row['Target']
                        newPriceDifference = 1.5 * oldPriceDifference
                        df.loc[index, 'Stop Loss'] = row['Target']
                        df.loc[index, 'Target'] = row['Entry'] - newPriceDifference
                        df.loc[index, 'Profits'] = (update['close'].values[0] - df.loc[index,'Entry']) / df.loc[index,'Entry'] * (-1) * df.loc[index,'Amount'] * df.loc[index, 'Leverage']
                        df.to_csv('./database/' + self.tickerName + '/trades.csv')

                    elif update['high'].values[0] > row['Stop Loss']:
                        df.loc[index, 'Outcome'] = 'Closed'
                        df.loc[index, 'Profits'] = (df.loc[index,'Stop Loss'] - df.loc[index, 'Entry']) / df.loc[index,'Entry'] * (-1) * df.loc[index, 'Amount'] * df.loc[index, 'Leverage']
                        df.to_csv('./database/' + self.tickerName + '/trades.csv')

        # TO-DO: If ticker is currently trading, do intervalAnalysis
        pass