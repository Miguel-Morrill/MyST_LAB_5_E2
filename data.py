
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
import functions as fun

data_E=pd.read_csv('BTC19_20.csv')
data_P=pd.read_csv('BTC20_21.csv')

data_ES = fun.tec1(data_E).dropna()
data_ES2 = fun.tec2(data_E).dropna()

vol=0.5 # volumen en bitcoin
pips=9000 # exposicion por operacion 100 usd
df = data_ES2[(data_ES2['stochastic_buy_signal']==True) | (data_ES2['stochastic_sell_signal']==True)] # df con las señales de compra y venta
transacciones = fun.transactions(vol, pips, df)