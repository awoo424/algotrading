from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

class App(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def historicalData(self, reqId, bar):
        print(f'Time: {bar.date} Close: {bar.close}')


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

# Create contracts - stocks
tsla_contract = Contract()
tsla_contract.symbol = "TSLA"
tsla_contract.secType = "STK"
tsla_contract.exchange = "ISLAND"
tsla_contract.currency = "USD"

# Create contracts - fx pairs
eurgbp_contract = Contract()
eurgbp_contract.symbol = "EUR"
eurgbp_contract.secType = "CASH"
eurgbp_contract.currency = "GBP"
eurgbp_contract.exchange = "IDEALPRO"

# Request historical bar data
# reqHistoricalData(tickerId, contract, endDateTime, durationString, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate)
app.reqHistoricalData(1, eurgbp_contract, '', '1 M', '1 day', 'ASK', 1, 1, False, None)

# Wait for incoming data
time.sleep(10)

app.disconnect()