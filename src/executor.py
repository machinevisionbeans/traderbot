import Pyro4
from datetime import datetime
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
    def execute(self, tickerName, action, quantity, stopLoss, takeProfit, leverage):
        # Check if connected
        self.app.checkConnection()
        #Place orders
        print('making order')
        #! Currently this will be executed as a market order since no limit price is given!
        self.app.makeOrder(tickerName, action, quantity, stopLoss, takeProfit)
        #Cancel order 
        # print('cancelling order')
        # app.cancelOrder(app.nextorderId)
        time.sleep(3)

        app.disconnect()
        print("(" + datetime.fromtimestamp(time.time()).strftime('%H:%M') + ") " + "Executed " + str(buySell) + " " + tickerName + " for $" + str(amount) + " at x" + str(leverage) + " leverage. Stop Loss = " + str(stopLoss) + ", Take Profit = " + str(takeProfit) + ".")


### MAIN CODE EXECUTION
Pyro4.config.MAX_RETRIES = 200
Pyro4.config.THREADPOOL_SIZE = 3000

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(Executor)   # register the greeting maker as a Pyro object
ns.register("executor", uri)
print("Server Created.")
daemon.requestLoop()