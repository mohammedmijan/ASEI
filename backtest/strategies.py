import backtrader as bt



class SmaCrossoverStochastic(bt.Strategy):
    params = dict(sma_fast_period=10, sma_slow_period=30,
                  stochastic_upperband=60, stochastic_lowerband=30)

    def __init__(self):
        sma_fast = bt.indicators.SMA(period=self.p.sma_fast_period)
        sma_slow = bt.indicators.SMA(period=self.p.sma_slow_period)
        self.crossover = bt.indicators.CrossOver(
            sma_fast, sma_slow)  # returns: -1, 0 or 1
        self.stochastic = bt.indicators.StochasticSlow(
            upperband=self.p.stochastic_upperband, lowerband=self.p.stochastic_lowerband)

    def next(self):
        close_price = self.data.close * 1.0
        position_size = self.position.size
        available_cash = self.broker.getcash() * 1

        if self.position.size:
            if self.crossover < 0 and self.stochastic <= self.p.stochastic_lowerband:
                print('- [{}] Closing {} position(s) at {}$'.format(
                    self.data.datetime.date(), position_size, close_price))
                self.close()
        elif self.crossover > 0 and self.stochastic >= self.p.stochastic_upperband:
            print('+ [{}] Buying {} position(s) at {}$'.format(
                self.data.datetime.date(), int(available_cash * 0.95 / close_price), close_price))
            self.buy(size=int(available_cash * 0.95 / close_price))

class RSI(bt.Strategy):
    param = [ 20 , 80 ]

    def __init__(self):
        self.rsi = bt.indicators.RSI_Safe(self.data.close, period=21)

    def next(self):
        if not self.position:
            if self.rsi < self.param[0]:
                close = self.data.close[0] # 종가 값 
                size = int(self.broker.getcash() / close)  # 최대 구매 가능 개수 
                
                self.buy(size=size)
        else:
            if self.rsi > self.param[1]:
                self.close() # 매

class MACD(bt.Strategy):
    '''
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:
      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)
     - Set a stop price x times the ATR value away from the close
     - If in the market:
       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    '''
    
    param = [ 12 , 26 , 9 ]
    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 15.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def __init__(self):
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.param[0],
                                       period_me2=self.param[1],
                                       period_signal=self.param[2])
        


        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        

        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)
        

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)
    


    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.mcross[0] > 0.0 and self.smadir < 0.0:
                
                close = self.data.close[0] # 종가 값 
                print("Buy at Closing Prize:{}".format(close))
                size = int(self.broker.getcash() / close)  # 최대 구매 가능 개수 
                print("Buy Size:{}".format(size))
                self.order = self.buy(size=size) # 매수 size = 구매 개수 설정 
                pdist = self.atr[0] * self.p.atrdist
                self.pstop = self.data.close[0] - pdist

        else:  # in the market
            pclose = self.data.close[0]
            pstop = self.pstop

            if pclose < pstop:
                print("Sell at:{}".format(pclose))
                self.close()  # stop met - get out
            else:
                pdist = self.atr[0] * self.p.atrdist
                # Update only if greater than
                self.pstop = max(pstop, pclose - pdist)
        
class BollingerBand(bt.Strategy):
    param = [20]
    params = (('BBandsperiod', 20),)

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.redline = None
        self.blueline = None

        # Add a BBand indicator
        self.bband = bt.indicators.BollingerBands(self.datas[0], period=self.param[0])
        

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        if self.dataclose < self.bband.lines.bot and not self.position:
        	self.redline = True

        if self.dataclose > self.bband.lines.top and self.position:
            self.blueline = True

        if self.dataclose > self.bband.lines.mid and not self.position and self.redline:        	
        	# BUY, BUY, BUY!!! (with all possible default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # Keep track of the created order to avoid a 2nd order
            close = self.data.close[0] # 종가 값 
            size = int(self.broker.getcash() / close)  # 최대 구매 가능 개수 
            
            self.order = self.buy(size=size)

        if self.dataclose > self.bband.lines.top and not self.position:
            # BUY, BUY, BUY!!! (with all possible default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            # Keep track of the created order to avoid a 2nd order
            
            close = self.data.close[0] # 종가 값 
            size = int(self.broker.getcash() / close)  # 최대 구매 가능 개수 
            
            self.order = self.buy(size=size)

        if self.dataclose < self.bband.lines.mid and self.position and self.blueline:
            # SELL, SELL, SELL!!! (with all possible default parameters)
            self.log('SELL CREATE, %.2f' % self.dataclose[0])
            self.blueline = False
            self.redline = False
            # Keep track of the created order to avoid a 2nd order
            self.order = self.close()




    
        

        