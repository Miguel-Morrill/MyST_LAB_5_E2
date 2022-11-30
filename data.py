
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

vol=4 # volumen en bitcoin
pip_tp=9000 # exposicion por operacion 100 usd
pip_sl=9000 # exposicion por operacion 100 usd
a=fun.capital(vol, pip_tp, pip_sl, df)

retorno_prueba=fun.capitalgrid(vol, pips, df)

# parametros postizos
vol_2=np.arange(.5,8,.5)
pips_2=np.arange(1000,100000,5000)

busqueda = fun.grid_search(vol_2, pips_2, pips_2, df)

maxSharp = busqueda.Sharpe.max()
best_param = busqueda.loc[busqueda.Sharpe==maxSharp]

data_PS2 = fun.tec2(data_P).dropna()

df_p = data_PS2[(data_PS2['stochastic_buy_signal']==True) | (data_PS2['stochastic_sell_signal']==True)] # df con las señales de compra y venta
a2=fun.capital(best_param.iloc[0,0], best_param.iloc[0,1],best_param.iloc[0,2], df_p)

transacciones_a2=fun.transactions_2(best_param.iloc[0,0], best_param.iloc[0,1],best_param.iloc[0,2], df_p)