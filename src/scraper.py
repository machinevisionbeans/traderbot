import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import os
from yahooquery import Ticker
from strategyCalculator import StrategyCalculator
from progressReport import progressReport as pr


class Scraper():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.stratCalc = StrategyCalculator(self.tickerName)
    
    def update(self):
        analysisChangePendingToVoid = True
        repeat = 0
        while True:
            repeat = repeat + 1
            self.scrape(analysisChangePendingToVoid)
            if repeat == 24:
                repeat = 0
                pr()

            analysisChangePendingToVoid = False
            t = datetime.utcnow()
            sleeptime = 300 - (t.second + t.microsecond/1000000.0)
            time.sleep(sleeptime + 60)

            

    def scrape(self, ChangePendingToVoid):

        tickers = Ticker(self.tickerName)
        df = tickers.history(period='7d', interval='1m')
        df = df.iloc[::-1]

        if os.path.exists('./database/' + self.tickerName):
            
            ##Change all previously unfinished analysis rows to 'void' on startup
            if ChangePendingToVoid == True:
                analysisRead = pd.read_csv('./database/' + self.tickerName + '/analysis.csv', index_col= 0)
                for index,row in analysisRead.iterrows():
                    if row['Outcome'] == 'Pending':
                        analysisRead.loc[index, 'Outcome'] = 'Void (Prog Closed)'
                analysisRead.to_csv('./database/' + self.tickerName + '/analysis.csv')

            ## This saving then re-reading is necessary to prevent the buggy header issues
            df.to_csv('./database/' + self.tickerName + '/temp.csv')
            df = pd.read_csv('./database/' + self.tickerName + '/temp.csv')
            ###########################
            dfFirstTwoRows = df.head(2)
            dfSecondRow = dfFirstTwoRows.iloc[1:].head(1)
            dfDate = dfSecondRow['date'].values[0]

            database = pd.read_csv('./database/' + self.tickerName + '/query.csv', index_col=0)
            databaseFirstTwoRow = database.head(2)
            databaseSecondRow = databaseFirstTwoRow.iloc[1:].head(1)
            dbDate = databaseSecondRow['date'].values[0]

            if not (dbDate == dfDate):
                print("Updating " + self.tickerName + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
                df.to_csv('./database/' + self.tickerName + '/query.csv')
                self.stratCalc.inform(df.iloc[1:])
        else:
            print("Creating and Updating " + self.tickerName + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
            os.makedirs('./database/' + self.tickerName + '/')
            analysisColumnNames = ['Time Stamp', 'Strategy', 'Position', 'Amount', 'Entry', 'Stop Loss', 'Take Profit', 'Outcome', 'Profits', 'Points Gained/Lost']
            analysisFrame = pd.DataFrame(columns=analysisColumnNames)
            analysisFrame.to_csv('./database/' + self.tickerName + '/analysis.csv')
            tradeColumnNames = ['Time Stamp', 'OrderId', 'Position', 'Amount', 'Quantity', 'Entry', 'Stop Loss', 'Target', 'Leverage', 'Outcome', 'Profits']
            tradeFrame = pd.DataFrame(columns=tradeColumnNames)
            tradeFrame.to_csv('./database/' + self.tickerName + '/trades.csv')
            df.to_csv('./database/' + self.tickerName + '/query.csv')
            df.to_csv('./database/' + self.tickerName + '/temp.csv')
            df = pd.read_csv('./database/' + self.tickerName + '/temp.csv')        
            self.stratCalc.inform(df.iloc[1:])

        pass
        
        
        
    
