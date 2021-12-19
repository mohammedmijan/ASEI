from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import pandas as pd
from strategies import BollingerBand
from strategies import MACD, SmaCrossoverStochastic, RSI
import yfinance as yf



if __name__ == '__main__':
    cerebro = bt.Cerebro(cheat_on_open=True)
    df = pd.read_csv("data/csv_data/stockmarket_modified.csv", parse_dates=True, index_col=0)
    data = bt.feeds.PandasData(dataname=df)
    #print(yf.download("FB"))
    cerebro.adddata(data)
    #cerebro.addstrategy(MACD)
    #cerebro.addstrategy(RSI)
    cerebro.addstrategy(BollingerBand)
    #cerebro.addstrategy(SmaCrossoverStochastic)
    #cerebro.addstrategy(TestStrategy)
    #cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="SharpeRatio")
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name="pyfolio")
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)  # sizer for strategies

    cerebro.broker.setcash(100000.00)
    #cerebro.broker.add_cash(1000.00)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    results = cerebro.run()
    
    #print(results[0].analyzers.getbyname("pyfolio").get_analysis()['positions'])
    #print(start.analyzers.getbyname("SharpeRatio").get_analysis()["sharperatio"])
    
    
    #print('Return Cash: %.5f' % cerebro.broker.get_cash())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
    