Introduction to Paper Trading
===============================

In this tutorial, you will learn:

* What is paper trading
* How to start paper trading with Interactive Brokers

Intro to paper trading
----------------------
.. admonition:: Definition
   :class: myOwnStyle

   | A **paper trade** is a simulated trade that allows an investor to practice 
     buying and selling without risking real money.

*Under construction*


Setup Interactive Brokers API
-----------------------------

*Under construction*


Connect to Interactive Brokers TWS
----------------------------------

::

    class App(EWrapper, EClient):
    
        def __init__(self):
            EClient.__init__(self, self)

    app = App()
    app.connect('127.0.0.1', 7497, 0)
    app.run()

    app.disconnect()

*Under construction*


Create Basic Contracts
----------------------

::

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

*Under construction*


Request Market Data
-------------------

Request Streaming Market Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    class App(EWrapper, EClient):

        # Receive market data
        def tickPrice(self, tickerId, field, price, attribs):
            print("Tick Price. Ticker Id:", tickerId, ", TickType: ", TickTypeEnum.to_str(field),
                  ", Price: ", price, ", CanAutoExecute: ", attribs.canAutoExecute,
                  ", PastLimit: ", attribs.pastLimit, ", PreOpen: ", attribs.preOpen)

    # Request market data
    app.reqMktData(1, tsla_contract, '', False, False, None)

Request Historical Market Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    class App(EWrapper, EClient):

        # Receive historical bar data
        def historicalData(self, reqId, bar):
            print("HistoricalData. ReqId:", reqId, "BarData.", bar)
    
    # Request historical bar data
    app.reqHistoricalData(1, eurgbp_contract, '', '1 M', '1 day', 'ASK', 1, 1, False, None)

*Under construction*


Manage Orders
-------------

::

  class App(EWrapper, EClient):

      def nextValidId(self, orderId: int):
          super().nextValidId(orderId)
          self.nextorderId = orderId
          print('The next valid order id is: ', self.nextorderId)

      def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, 
                      lastFillPrice, clientId, whyHeld, mktCapPrice):
          print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled,
                ", Remaining: ", remaining, ", AvgFillPrice: ", avgFillPrice,
                ", PermId: ", permId, ", ParentId: ", parentId, ", LastFillPrice: ", lastFillPrice,
                ", ClientId: ", clientId, ", WhyHeld: ", whyHeld, ", MktCapPrice: ", mktCapPrice)

      def openOrder(self, orderId, contract, order, orderState):
          print("OpenOrder. PermID: ", order.permId, ", ClientId: ", order.clientId,
                ", OrderId: ", orderId, ", Account: ", order.account, ", Symbol: ", contract.symbol, 
                ", SecType: ", contract.secType, " , Exchange: ", contract.exchange,
                ", Action: ", order.action, ", OrderType: ", order.orderType,
                ", TotalQty: ", order.totalQuantity, ", CashQty: ", order.cashQty,
                ", LmtPrice: ", order.lmtPrice, ", AuxPrice: ", order.auxPrice,
                ", Status: ", orderState.status)

      def execDetails(self, reqId, contract, execution):
          print("ExecDetails. ", reqId, " - ", contract.symbol, ", ", contract.secType,
                ", ", contract.currency, " - ", execution.execId, ", ", execution.orderId,
                ", ", execution.shares , ", ", execution.lastLiquidity)

Place Orders
^^^^^^^^^^^^

::

    # Place order
    app.placeOrder(app.nextorderId, eurgbp_contract, order)


Modify Orders
^^^^^^^^^^^^^

:: 

    # Modify order
    order_id = 20
    order.lmtPrice = '0.82'
    app.placeOrder(order_id, eurgbp_contract, order)


Cancel Orders
^^^^^^^^^^^^^

:: 

    # Cancel order by order Id
    app.cancelOrder(app.nextorderId)

    # Cancel all open orders
    app.reqGlobalCancel()

*Under construction*



Request Account Summary
-----------------------

::
    
    class App(EWrapper, EClient):

        # Receive account summary
        def accountSummary(self, reqId:int, account:str, tag:str, value:str, currency:str):
              print("Acct Summary. ReqId:" , reqId , "Acct:", account, "Tag: ", tag, "Value:", value, 
                    "Currency:", currency)

    # Request account summary in base currency
    app.reqAccountSummary(9002, "All", "$LEDGER");

    # Request account summary in HKD
    app.reqAccountSummary(9002, "All", "$LEDGER:HKD");

*Under construction*


**References**
(TO-EDIT)

* `Investopedia - Paper Trade <https://www.investopedia.com/terms/p/papertrade.asp/>`_


.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.