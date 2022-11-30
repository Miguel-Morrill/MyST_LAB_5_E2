
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: PROYECTO: ANALISIS TÉCNICO                                                        -- #                                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/Miguel-Morrill/MyST_LAB_5_E2.git                                                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

from datetime import datetime
#import MetaTrader5 as mt5
import pandas as pd
import pytz
import numpy as np
from ta.volatility import BollingerBands
from ta.momentum import StochasticOscillator
from ta.trend import MACD
import plotly.express as px

'''
def import_data():
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
    quit()
    # set time zone to UTC
    
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime(2020, 2, 1, tzinfo=timezone)
    utc_to = datetime(2021, 2, 1, tzinfo=timezone)
    # get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
    rates = mt5.copy_rates_range("BITCOIN", mt5.TIMEFRAME_D1, utc_from, utc_to)

    
    # create DataFrame out of the obtained data
    rates_frame = pd.DataFrame(rates)
    # convert time in seconds into the 'datetime' format
    #rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    
    rates_frame
    #rates_frame.to_csv('BTC20_21.csv')
    
    return rates_frame
'''

# Boolinger
def tec1(data):
    df = data.copy()
    indicator_bb = BollingerBands(close=data.close, window=21)
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()
    df['bb_high_signal'] = indicator_bb.bollinger_hband_indicator()
    df['bb_low_signal'] = indicator_bb.bollinger_lband_indicator()
    return df

# RSI
def tec2(data):
    df = data.copy()
    indicator_stoc = StochasticOscillator(high=data['high'], low=data['low'], close=data['close'])
    df['stochastic'] = indicator_stoc.stoch()
    df['stochastic_buy_signal'] = indicator_stoc.stoch() < 20
    df['stochastic_sell_signal'] = indicator_stoc.stoch() > 80
    return df

def Average(lst):
    return sum(lst) / len(lst)

def transactions(vol, pips, df):
    rett=[]
    
    while len(df)>2:
        precio_transaccion=df['close'].iloc[0]
        posicion=precio_transaccion*vol
        day0=df.iloc[0,0]

        closed=df[(df['close']>=(precio_transaccion+pips/100))|(df['close']<=(precio_transaccion-pips/100))]
        closed_price=closed.iloc[0,5]
        closed_transaction= closed_price*vol
        day1=closed.iloc[0,0]

        ret=246*(closed_transaction/posicion-1)/(day1-day0)

        rett.append(ret)

        df=df.loc[closed.iloc[0,0]:]
    
    return rett

def capital(vol, pip_tp, pip_sl, df):
    dayss=[]
    cashh=[]
    cash=100000
    while len(df)>2:
        precio_transaccion=df['close'].iloc[0]
        posicion=precio_transaccion*vol
        cash=cash-posicion
        day0=df.iloc[0,0]

        closed=df[(df['close']>=(precio_transaccion+pip_tp/100))|(df['close']<=(precio_transaccion-pip_sl/100))]
        closed_price=closed.iloc[0,5]
        closed_transaction= closed_price*vol

        cash=cash+closed_transaction
        cashh.append(cash)
        df=df.loc[closed.iloc[0,0]:]
        dayss.append(day0)
    
    dff = pd.DataFrame(dict(
    days = dayss,
    capital = cashh))
    
    return dff

def capitalgrid(vol, pips, df):
    dayss=[]
    cashh=[]
    cash=100000
    while len(df)>2:
        precio_transaccion=df['close'].iloc[0]
        posicion=precio_transaccion*vol
        cash=cash-posicion
        day0=df.iloc[0,0]

        closed=df[(df['close']>=(precio_transaccion+pips/100))|(df['close']<=(precio_transaccion-pips/100))]
        closed_price=closed.iloc[0,5]
        closed_transaction= closed_price*vol

        cash=cash+closed_transaction
        cashh.append(cash)
        df=df.loc[closed.iloc[0,0]:]
        dayss.append(day0)
    
    dff = pd.DataFrame(dict(
    days = dayss,
    capital = cashh))
    
    return dff.iloc[-1,1]

# For i,j loop es un grid search
# Podemos usar un gridsearch sin PSO
def grid_search(vol, pip_sl, pip_tp, df):
    #Create dataframe
    dif_port = pd.DataFrame()
    sl_list = []
    tp_list = []
    max_loss_list = []
    Sharpe_list = []
    #Iterate with different parameteres
    for i in vol:
        for j in pip_sl:
            for k in pip_tp:
                ent_capital = capital(i, j, k, df)
                #Obtaining the sharpe ratio
                Portfolio = pd.DataFrame()
                Portfolio["Portfolio Value"] = ent_capital.iloc[:,1]
                Portfolio["Return"] = Portfolio["Portfolio Value"].pct_change(1)
                Sharpe= Portfolio["Return"].mean() /Portfolio["Return"].std()
                sl_list.append(j)
                tp_list.append(k)
                max_loss_list.append(i)
                Sharpe_list.append(Sharpe)  
    
    dif_port["Volume"] = max_loss_list
    dif_port["Stop Loss"] = sl_list
    dif_port["Take profit"] = tp_list
    dif_port["Sharpe"] = Sharpe_list
    return dif_port

def transactions_2(vol, pip_tp, pip_sl, df):
    rett=[]
    
    while len(df)>2:
        precio_transaccion=df['close'].iloc[0]
        posicion=precio_transaccion*vol
        day0=df.iloc[0,0]

        closed=df[(df['close']>=(precio_transaccion+pip_tp/100))|(df['close']<=(precio_transaccion-pip_sl/100))]
        closed_price=closed.iloc[0,5]
        closed_transaction= closed_price*vol
        day1=closed.iloc[0,0]

        ret=246*(closed_transaction/posicion-1)/(day1-day0)

        rett.append(ret)

        df=df.loc[closed.iloc[0,0]:]
    
    return rett

