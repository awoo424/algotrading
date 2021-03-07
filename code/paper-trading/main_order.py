from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time


class App(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print('Order Status - orderId:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining,
              'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('Open Order id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)


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

# Create contracts - fx pairs
eurgbp_contract = Contract()
eurgbp_contract.symbol = "EUR"
eurgbp_contract.secType = "CASH"
eurgbp_contract.currency = "GBP"
eurgbp_contract.exchange = "IDEALPRO"

# Create orders
order = Order()
order.action = 'BUY'
order.totalQuantity = 20000
order.orderType = 'LMT'
order.lmtPrice = '0.84'

# Place order
# placeOrder(orderId, contract, order)
print('placing order')
app.placeOrder(app.nextorderId, eurgbp_contract, order)

time.sleep(5)

# Modify order
#print('modifying order')
#order_id = 20
#order.lmtPrice = '0.82'
#app.placeOrder(order_id, eurgbp_contract, order)

#time.sleep(3)

# Cancel order by order Id
print('cancelling order')
app.cancelOrder(app.nextorderId)

# Cancel all open orders
#print('cancelling all open orders')
#app.reqGlobalCancel()

time.sleep(3)
app.disconnect()