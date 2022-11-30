
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