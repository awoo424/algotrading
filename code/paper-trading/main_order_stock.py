from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time
from datetime import date


class App(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice,
                    clientId, whyHeld, mktCapPrice):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining,
                ", AvgFillPrice: ", avgFillPrice, ", PermId: ", permId, ", ParentId: ", parentId, ", LastFillPrice: ",
              lastFillPrice, ", ClientId: ", clientId, ", WhyHeld: ", whyHeld, ", MktCapPrice: ", mktCapPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. PermID: ", order.permId, ", ClientId: ", order.clientId, ", OrderId: ", orderId, ", Account: ", order.account, ", Symbol: ", contract.symbol, ", SecType: ",
              contract.secType, " , Exchange: ", contract.exchange, ", Action: ", order.action, ", OrderType: ",
              order.orderType, ", TotalQty: ", order.totalQuantity, ", CashQty: ", order.cashQty, ", LmtPrice: ",
              order.lmtPrice, ", AuxPrice: ", order.auxPrice, ", Status: ", orderState.status)


    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, " - ", contract.symbol, ", ", contract.secType, ", ", contract.currency,
              " - ", execution.execId, ", ", execution.orderId, ", ", execution.shares , ", ", execution.lastLiquidity)


def run_loop():
    app.run()

app = App()
app.connect('127.0.0.1', 7497, 0)

app.nextorderId = None

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop)
api_thread.start()

# Allow time for server connection
time.sleep(1)

# Create contracts - HK stock
contract = Contract()
contract.symbol = "1"
contract.secType = "STK"
contract.exchange = "SEHK"
contract.currency = "HKD"

# Create orders
order = Order()    
order.action = 'BUY'
order.totalQuantity = 500
order.orderType = 'MKT'
    
today = date.today()
today = today.strftime("%Y%m%d")
print(today)
order.goodAfterTime = today + " 16:29:00 "

# Place order
print('Placing order')
app.placeOrder(app.nextorderId, contract, order)

time.sleep(5)

"""
# Modify order
print('Modifying order')
order_id = 20
order.lmtPrice = '0.82'
app.placeOrder(order_id, eurgbp_contract, order)

time.sleep(5)
"""

# Cancel order by order Id
print('Cancelling order')
app.cancelOrder(app.nextorderId)

"""
# Cancel all open orders
print('Cancelling all open orders')
app.reqGlobalCancel()
"""

time.sleep(5)
app.disconnect()