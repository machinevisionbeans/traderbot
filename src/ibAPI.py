from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.execution import Execution
from ibapi.commission_report import CommissionReport

from IBanalyser import IBAnalyser

import threading
import time
import logging

# TODO 
# Make a base class of ibAPI with the generic function names in case we 
# switch to a differnt platform in the future
#class Platform():

#Empty 'struct' for Contracts and Orders
# class Contract():
#     pass

# class Order():
#     pass

class ibAPI(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)
        self.nextorderId = None
        self.postExec = IBAnalyser()

    '''    
    Connect to TWS
    '''
    def connectPlatform(self):
        self.connect('127.0.0.1', 7497, 123) # Change port no to match port no in IB settings

    def connectionClosed(self): # called by TWS after self.disconnect()
        print("Connection Closed")

    def nextValidId(self, orderId: int): # called by TWS on startup and self.reqIDs(no)
        self.nextorderId = orderId # This is automatically done on connection
        print('The next valid order id is: ', self.nextorderId)
    
    # Use this to increment orderIDs on our end, so request to TWS for order IDs dont need to be made.
    def obtainNextValidOrderIDs(self, number=1):
        nextID = self.nextorderId
        self.nextorderId += number
        return nextID

    def checkConnection(self):
        if not self.isConnected():
            print("TWS Not connected. Connecting...")
            self.nextorderId = None
            self.connectPlatform()
            time.sleep(1)
            while True:
                if isinstance(self.nextorderId, int):
                    print('connected')
                    print()
                    break
                else:
                    print('waiting for connection')
                    time.sleep(1)

    # General fn
    def Start(self):
        while not self.isConnected():
            print("Connecting to IB Host...")
            self.connectPlatform()
            time.sleep(1)
        print("Starting IB API Thread...")
        ibAPIthread = threading.Thread(target=self.run, daemon=True)
        ibAPIthread.start()
        #Check if the API is connected via orderid
        while True:
            if isinstance(self.nextorderId, int):
                print('connected')
                print()
                break
            else:
                print('waiting for connection')
                time.sleep(1)
    '''    
    Contracts
    '''
    def CreateContract(self, security, securityType='STK', exchange='SMART', currency='USD'):
        # Check if this is Stock or Forex
        if len(security) > 5:
            currency = security[3:6]
            security = security[0:3]
            securityType = 'CASH'
        contract = Contract()
        contract.symbol = security
        contract.secType = securityType
        contract.exchange = exchange
        contract.currency = currency
        return contract
    
    '''    
    Defining Orders
    '''
    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract:Contract, execution:Execution):
    #     class Execution(Object):
    # def __init__(self):
    #     self.execId = ""
    #     self.time =  ""
    #     self.acctNumber =  ""
    #     self.exchange =  ""
    #     self.side = ""
    #     self.shares = 0.
    #     self.price = 0. 
    #     self.permId = 0
    #     self.clientId = 0
    #     self.orderId = 0
    #     self.liquidation = 0
    #     self.cumQty = 0.
    #     self.avgPrice = 0.
    #     self.orderRef =  ""
    #     self.evRule =  ""
    #     self.evMultiplier = 0.
    #     self.modelCode =  ""
    #     self.lastLiquidity = 0

        self.postExec.executed(tickerName=contract.symbol, orderId=execution.orderId, execPrice=execution.avgPrice, execTotalQty=execution.cumQty)

        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    def commissionReport(self, commissionReport:CommissionReport):
    #     class CommissionReport(Object):
    # def __init__(self):
    #     self.execId = ""
    #     self.commission = 0. 
    #     self.currency = ""
    #     self.realizedPNL =  0.
    #     self.yield_ = 0.
    #     self.yieldRedemptionDate = 0  # YYYYMMDD format
        pass

    #! Market Order
    def MarketOrder(self, action, quantity):
        order = Order()
        order.action = action
        order.orderType = "MKT"
        order.totalQuantity = quantity
        return order

    #! Limit Order
    # A Limit order is an order to buy or sell at a specified price or better. The Limit order ensures that if the order fills, 
    # it will not fill at a price less favorable than your limit price, but it does not guarantee a fill. 
    def LimitOrder(self, action, quantity, limitPrice):
        order = Order()
        order.action = action
        order.orderType = "LMT"
        order.totalQuantity = quantity
        order.lmtPrice = limitPrice
        return order

    #! Stop Order
    #? Will immediately try and buy/sell if the market hits that price,
    #? but will also execute even if it overshoots by a lot
    #? i.e. If the price suddenly falls by a lot past the price, it will execute the order at a very low price
    # A Stop order is an instruction to submit a buy or sell market order if and when the user-specified stop trigger price is attained or penetrated. 
    # A Stop order is not guaranteed a specific execution price and may execute significantly away from its stop price. 
    # A Sell Stop order is always placed below the current market price and is typically used to limit a loss or protect a profit on a long stock position. 
    # A Buy Stop order is always placed above the current market price. 
    # It is typically used to limit a loss or help protect a profit on a short sale. 
    def StopOrder(self, action, quantity, stopPrice):
        order = Order()
        order.action = action
        order.orderType = "STP"
        order.totalQuantity = quantity
        order.auxPrice = stopPrice
        return order

    #! Stop Limit Order
    #? Will try to execute the order at the limit price executed, but no guarentees
    #? i.e. If the price drops a lot suddenly, it may not be able to stop loss/take profit at all
    def StopLimitOrder(self, action, quantity, stopPrice, limitPrice):
        order = Order()
        order.action = action
        order.orderType = "STP LMT"
        order.totalQuantity = quantity
        order.auxPrice = stopPrice
        order.lmtPrice = limitPrice
        return order

    #! Trailing Stop
    def TrailingStopOrder(self, action, quantity, isPercentage:bool, trailingAmount, trailStopPrice):
        order = Order()
        order.action = action
        order.orderType = "TRAIL"
        order.totalQuantity = quantity
        order.trailStopPrice = trailStopPrice
        if isPercentage:
            order.trailingPercent = trailingAmount
        else:
            order.auxPrice = trailingAmount
        return order
    
    #! Trailing Stop Limit
    #? The limit price also moves by offset amount
    def TrailingStopLimitOrder(self, action, quantity, isPercentage:bool, trailingAmount, trailStopPrice, lmtPriceOffset):
        order = Order()
        order.action = action
        order.orderType = "TRAIL LIMIT"
        order.totalQuantity = quantity
        order.trailStopPrice = trailStopPrice
        order.lmtPriceOffset = lmtPriceOffset
        if isPercentage:
            order.trailingPercent = trailingAmount
        else:
            order.auxPrice = trailingAmount
        return order

    # IB does not directly have an order that can set a buy/sell price, stop loss price and take profit price at once
    # so we need to chain 3 orders together
    # Once one of the parent orders is cancelled, the other child orders are automatically cancelled

    #! Bracket Limit Order with Stop Loss and Take Profit
    def BracketLimitStopLossTakeProfit(self, action, quantity, limitPrice, takeProfitPrice, stopLossPrice):

        oppAction = "BUY" if action == "SELL" else "SELL"

        # reserve the next 3 order IDs
        nextID = self.obtainNextValidOrderIDs(3)

        # Create Limit Order
        ParentOrder = self.LimitOrder(action=action, quantity=quantity, limitPrice=limitPrice)
        ParentOrder.orderId = nextID
        ParentOrder.transmit = False

        # Create Take Profit (Limit Order)
        TakeProfit = self.LimitOrder(action=oppAction, quantity=quantity, limitPrice=takeProfitPrice)
        TakeProfit.orderId = ParentOrder.orderId + 1
        TakeProfit.transmit = False
        TakeProfit.parentId = ParentOrder.orderId

        # Create Stop Loss (Stop Order)
        StopLoss = self.StopOrder(action=oppAction, quantity=quantity, stopPrice=stopLossPrice)
        StopLoss.orderId = ParentOrder.orderId + 2
        StopLoss.transmit = True
        StopLoss.parentId = ParentOrder.orderId

        bracketOrder = [ParentOrder, TakeProfit, StopLoss]
        return bracketOrder	

    #! Bracket Market Order with Stop Loss and Take Profit
    def BracketMktStopLossTakeProfit(self, action, quantity, takeProfitPrice, stopLossPrice):

        oppAction = "BUY" if action == "SELL" else "SELL"

        # reserve the next 3 order IDs
        nextID = self.obtainNextValidOrderIDs(3)

        # Create Limit Order
        ParentOrder = self.MarketOrder(action=action, quantity=quantity)
        ParentOrder.orderId = nextID
        ParentOrder.transmit = False

        # Create Take Profit (Limit Order)
        TakeProfit = self.LimitOrder(action=oppAction, quantity=quantity, limitPrice=takeProfitPrice)
        TakeProfit.orderId = ParentOrder.orderId + 1
        TakeProfit.transmit = False
        TakeProfit.parentId = ParentOrder.orderId

        # Create Stop Loss (Stop Order)
        StopLoss = self.StopOrder(action=oppAction, quantity=quantity, stopPrice=stopLossPrice)
        StopLoss.orderId = ParentOrder.orderId + 2
        StopLoss.transmit = True
        StopLoss.parentId = ParentOrder.orderId

        bracketOrder = [ParentOrder, TakeProfit, StopLoss]
        return bracketOrder	

    #! Custom Bracket Order
    def CustomBracketOrder(self, Parent, Child1, Child2):
        # reserve the next 3 order IDs
        nextID = self.obtainNextValidOrderIDs(3)
        Parent.orderID = nextID
        Parent.transmit = False
        Child1.orderID = Parent.orderID + 1
        Child1.transmit = False
        Child2.orderID = Parent.orderID + 2
        Child2.transmit = True
        bracketOrder = [Parent, Child1, Child2]
        return bracketOrder

    '''    
    Executing Orders
    '''
    def makeOrder(self, tickerName, action, quantity, limitPrice, takeProfit, stopLoss):
        bracket = self.BracketLimitStopLossTakeProfit(action, quantity, limitPrice, takeProfit, stopLoss)
        for o in bracket:
            print("place order")
            self.placeOrder(o.orderId, self.CreateContract(tickerName), o)
        # time.sleep(3)
        print('Finished buy order')
        return bracket[0].orderId

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ibAPI()
    app.Start()

    #Place orders
    app.makeOrder("AAPL", "BUY", 100, 1, 500, 10)

    #Cancel order 
    # print('cancelling order')
    # app.cancelOrder(app.nextorderId)
    time.sleep(3)

    app.disconnect()

    time.sleep(3)