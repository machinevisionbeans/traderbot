import Pyro4
from datetime import datetime
import pandas as pd
from ibAPI import ibAPI
import time

## RUN THIS FIRST on command line
## for namespace
## pyro4-ns [options]
 ##


class Executor():
    app = ibAPI()
    app.Start()

    def __init__(self):
        pass
        
    
    @Pyro4.expose
    @Pyro4.oneway
    def execute(self, tickerName, action, quantity, limitPrice, stopLoss, takeProfit, leverage):
        # Check if connected
        self.app.checkConnection(2)
        #Place orders
        print('making order')
        orderId = self.app.makeOrder(tickerName, action, quantity, limitPrice, stopLoss, takeProfit)

        timestamp = datetime.fromtimestamp(time.time()).strftime('%H:%M')
        tradeWindow = pd.read_csv('./database/' + tickerName + '/trades.csv', index_col= 0)
        tradeWindow = tradeWindow.append({'Time Stamp' : timestamp, 'orderId': orderId, 'Position': action, 'Amount': (quantity * limitPrice), 'Quantity': quantity, 'Entry': limitPrice, 'Stop Loss': stopLoss, 'Target': takeProfit, 'Leverage': leverage, 'Outcome': 'Sent', 'Profits': 0}, ignore_index = True)
        tradeWindow.to_csv('./database/' + tickerName + '/trades.csv')

        print("(" + datetime.fromtimestamp(time.time()).strftime('%H:%M') + ") " + "Sent " + str(action) + " " + tickerName + " for $" + str(limitPrice) + " at x" + str(leverage) + " leverage. Stop Loss = " + str(stopLoss) + ", Take Profit = " + str(takeProfit) + ".")


### MAIN CODE EXECUTION
Pyro4.config.MAX_RETRIES = 200
Pyro4.config.THREADPOOL_SIZE = 3000

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(Executor)   # register the greeting maker as a Pyro object
ns.register("executor", uri)
print("Server Created.")
daemon.requestLoop()