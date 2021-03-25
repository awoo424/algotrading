Introduction to Paper Trading
===============================

.. highlight:: Python
  
In this tutorial, you will learn:

* What is paper trading
* How to start paper trading with Interactive Brokers

Intro to paper trading
----------------------
.. admonition:: Definition
   :class: myOwnStyle

   | A **paper trade** is a simulated trade that allows an investor to practice 
     buying and selling without risking real money.

| In this module, we will first set up a connection to Interactive Brokers Trader 
  Workstation (IB TWS). 

| Then, we will learn how to create basic contracts, request market data, manage
  orders, and request account summary. 


Setup Interactive Brokers API
-----------------------------
| Before setting up a connection to IB TWS, there are few tasks to be completed: 

1. Visit `InteractiveBrokers <https://www.interactivebrokers.com.hk/en/home.php>`_ website, and open an account
2. Download IB API software from `InteractiveBrokers GitHub account <http://interactivebrokers.github.io/>`_
3. Download TWS software from `InteractiveBrokers TWS <https://www.interactivebrokers.com/en/index.php?f=16042>`_
4. Choose an IDE that you code in
5. Subscribe to market data

| For detailed instructions, please refer to `InteractiveBrokers Initial Setup <https://interactivebrokers.github.io/tws-api/initial_setup.html>`_.


Connect to Interactive Brokers TWS
----------------------------------
| Once finish the setup, it's time to connect to IB TWS. Use :code:`app.connect()`
  to establish an API connection.

::

    class App(EWrapper, EClient):
    
        def __init__(self):
            EClient.__init__(self, self)

    # Establish API connection
    # app.connect(ipAddress, portNumber, clientId)
    app = App()
    app.connect('127.0.0.1', 7497, 0)
    app.run()

| If you are successfully connected to IB TWS, you will get the below output in your
  terminal. 

.. figure:: ../images/tws_connection_terminal.png
    :width: 400px
    :alt: "Terminal output."


Create Basic Contracts
----------------------
| Then, let's create basic contract objects (trading instruments) such as stocks, 
  or fx pairs.

::

    from ibapi.contract import Contract

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


Request Market Data
-------------------
| Using the contract objects, we can request both streaming and historical market data. 

Request Streaming Market Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| Use :code:`app.reqMktData()` to request streaming market data.

::

    class App(EWrapper, EClient):

        # Receive market data
        def tickPrice(self, tickerId, field, price, attribs):
            print("Tick Price. Ticker Id:", tickerId, ", TickType: ", TickTypeEnum.to_str(field),
                  ", Price: ", price, ", CanAutoExecute: ", attribs.canAutoExecute,
                  ", PastLimit: ", attribs.pastLimit, ", PreOpen: ", attribs.preOpen)

    # Request market data
    # app.reqMktData(tickerId, contract, genericTickList, snapshot, regulatorySnaphsot, mktDataOptions)
    app.reqMktData(1, tsla_contract, '', False, False, None)

| Note that if you haven't subscribed the market data, you will receive 10-15 minute 
  delayed streaming data. Before getting the delayed streaming data, make sure you use
  :code:`app.reqMarketDataType(3)` to switch market data type to delayed data.

::

    # Switch market data type
    # 3 for delayed data
    app.reqMarketDataType(3)

Request Historical Market Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| Use :code:`app.reqHistoricalData()` to request historical bar data.

::

    class App(EWrapper, EClient):

        # Receive historical bar data
        def historicalData(self, reqId, bar):
            print("HistoricalData. ReqId:", reqId, "BarData.", bar)
    
    # Request historical bar data
    # app.reqHistoricalData(tickerId, contract, endDateTime, durationString, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate)
    app.reqHistoricalData(1, eurgbp_contract, '', '1 M', '1 day', 'ASK', 1, 1, False, None)


Manage Orders
-------------
| Now, let's try to make an order!

| First, write some methods in EWrapper that are required for receiving all relevant
  information on order opening, order status, and order execution.    

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
| To place an order, use :code:`app.placeOrder()` to submit an order.

::

    # Place order
    # app.placeOrder(orderId, contract, order)
    app.placeOrder(app.nextorderId, eurgbp_contract, order)


Modify Orders
^^^^^^^^^^^^^
| To modify the order, call :code:`app.placeOrder()` again with the order id to be 
  modified and the updated parameters. 

:: 

    # Modify order
    order_id = 1
    order.lmtPrice = '0.82'
    app.placeOrder(order_id, eurgbp_contract, order)


Cancel Orders
^^^^^^^^^^^^^
| To cancel an order by its order id, use :code:`app.cancelOrder()`.

| To cancel all open orders, use :code:`app.reqGlobalCancel()`.

:: 

    # Cancel order by order Id
    app.cancelOrder(app.nextorderId)

    # Cancel all open orders
    app.reqGlobalCancel()


Request Account Summary
-----------------------
| Lastly, use :code:`app.reqAccountSummary()` to get the summarized account information.

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


**References**

* `Investopedia - Paper Trade <https://www.investopedia.com/terms/p/papertrade.asp/>`_
* `Trader Workstation API <https://interactivebrokers.github.io/tws-api/>`_

.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.