from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from daily_trading_strategy import main as run_daily_trading_strategy

import threading
import datetime, time
from datetime import date
import os
import pandas as pd

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

# Connect to IB TWS
app = App()
app.connect('127.0.0.1', 7497, 0)

app.nextorderId = None

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop)
api_thread.start()

# Allow time for server connection
time.sleep(1)

# Call main() function in daily_trading_strategy.py to capture signal
run_daily_trading_strategy()

# Read in today's signal
dir_name = os.getcwd() + '/database/daily_trading_data/'
    
# Set ticker to trade
ticker = "0001"
result_path = os.path.join(dir_name,'signal/' + ticker.zfill(4) + '-signal.csv')
df = pd.read_csv(result_path)

# Create contracts - HK stock
today = date.today()
today = today.strftime("%Y%m%d")
contract = Contract()
contract.symbol = "1" # 0001.HK
contract.secType = "STK"
contract.exchange = "SEHK"
contract.currency = "HKD"

order = Order()

print("\n")
print("############ Summary ############")
print("Today's signal is: " + str(df['signal'].iloc[0]))

# BUY signal detected
if (df['signal'].iloc[0] == 1):

    # Create BUY order    
    order.action = 'BUY'
    order.totalQuantity = 500
    order.orderType = 'MKT'
    
    print(today)
    order.goodAfterTime = today + " 16:29:00 "

    print('Placing BUY order...')
    app.placeOrder(app.nextorderId, contract, order)

# SELL signal detected
elif (df['signal'].iloc[0] == -1):
    
    # Create SELL order
    order.action = 'SELL'
    order.totalQuantity = 500
    order.orderType = 'MKT'
    
    order.goodAfterTime = today + " 16:29:00 "

    print('Placing SELL order...')
    app.placeOrder(app.nextorderId, contract, order)

else:
    print('As signal == 0, no order is made.')

time.sleep(5)
app.disconnect()