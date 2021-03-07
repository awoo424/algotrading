from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

class App(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 1 and reqId == 1:
            print('The current bid price is: ', price)
        if tickType == 2 and reqId == 1:
            print('The current ask price is: ', price)
        if tickType == 9 and reqId == 1:
            print('The current close price is: ', price)
        if tickType == 14 and reqId == 1:
            print('The current open price is: ', price)

        if tickType == 66 and reqId == 1:
            print('The delayed bid price is: ', price)
        if tickType == 67 and reqId == 1:
            print('The delayed ask price is: ', price)
        if tickType == 68 and reqId == 1:
            print('The delayed last price is: ', price)
        if tickType == 72 and reqId == 1:
            print('The delayed high price is: ', price)
        if tickType == 73 and reqId == 1:
            print('The delayed low price is: ', price)
        if tickType == 75 and reqId == 1:
            print('The delayed close price is: ', price)
        if tickType == 76 and reqId == 1:
            print('The delayed open price is: ', price)


def run_loop():
	app.run()

# Establish API connection
# connect(ip address, port number, client id)
app = App()
app.connect('127.0.0.1', 7497, 0)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop)
api_thread.start()

# Allow time for server connection
time.sleep(1)

# Switch market data type
# 3 for delayed data
app.reqMarketDataType(3)

# Create contracts - stocks
tsla_contract = Contract()
tsla_contract.symbol = 'TSLA'
tsla_contract.secType = 'STK'
tsla_contract.exchange = 'ISLAND'
tsla_contract.currency = 'USD'

# Create contracts - stocks
sunhungkai_contract = Contract()
sunhungkai_contract.symbol = '16'
sunhungkai_contract.secType = 'STK'
sunhungkai_contract.exchange = 'SEHK'
sunhungkai_contract.currency = 'HKD'

# Request Market Data
# reqMktData(tickerId, contract, genericTickList, snapshot, regulatorySnaphsot, mktDataOptions)
app.reqMktData(1, tsla_contract, '', False, False, None)

# Wait for incoming data
time.sleep(5)

app.disconnect()