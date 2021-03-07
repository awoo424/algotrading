from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

class App(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def accountSummary(self, reqId:int, account:str, tag:str, value:str, currency:str):
        print("Acct Summary. ReqId:" , reqId , "Acct:", account, "Tag: ", tag, "Value:", value, "Currency:", currency)

def run_loop():
    app.run()

app = App()
app.connect('127.0.0.1', 7497, 0)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop)
api_thread.start()

time.sleep(1)

# Account summary in base currency
app.reqAccountSummary(9002, "All", "$LEDGER");

# Account summary in HKD
app.reqAccountSummary(9002, "All", "$LEDGER:HKD");


time.sleep(3)
app.disconnect()