#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 12:53:55 2024

Strategy 2: Intraday Resistance Breakout

@author: Muykheng Long
"""

import pandas as pd
import numpy as np
import datetime
import copy
import matplotlib.pyplot as plt
import yfinance as yf

def ATR(DF, n=14):
    df = DF.copy()
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = df['High'] - df['Close'].shift(1)
    df['L-PC'] = df['Low'] - df['Close'].shift(1)
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(n).mean()
    #   df['ATR'] = df['TR'].ewm(com=n, min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return df2['ATR']

def CAGR(DF):
    df = DF.copy()
    df['cum_return'] = (1+df['ret']).cumprod()
    n = len(df)/(252*78)
    CAGR = (df['cum_return'].iloc[-1])**(1/n)-1
    return CAGR

def volatility(DF):
    df = DF.copy()
#    df['ret'] = df['Close'].pct_change()
    vol = df['ret'].std() * np.sqrt(252*78)
    return vol

def sharpe(DF, rf):
    sharpe = (CAGR(DF) - rf)/volatility(DF)
    return sharpe    

def max_dd(DF):
    df = DF.copy()
    df['cum_return'] = (1+df['ret']).cumprod()
    df['cum_rolling_max'] = df['cum_return'].max()
    df['drawdown'] = df['cum_rolling_max'] - df['cum_return']
    return (df['drawdown']/ df['cum_rolling_max']).max()



# Download data
tickers = ['MSFT','AAPL','META','AMZN','INTC','CSCO','VZ','IBM','TSLA','AMD'] 

ohlc_intraday = {}

for ticker in tickers: 
    temp = yf.download(ticker,period='1mo',interval='5m')
    temp.dropna(how='any',inplace=True)
    ohlc_intraday[ticker] = temp
    
# Calculate ATR and rolling max and min of close price and rolling max of volume for each stock 
ohlc_dic = copy.deepcopy(ohlc_intraday)
tickers_signal = {}
tickers_ret = {}
for ticker in tickers:
    ohlc_dic[ticker]['ATR'] = ATR(ohlc_dic[ticker],20)
    ohlc_dic[ticker]['roll_max_cp'] = ohlc_dic[ticker]['Close'].rolling(20).max()
    ohlc_dic[ticker]['roll_min_cp'] = ohlc_dic[ticker]['Close'].rolling(20).min()
    ohlc_dic[ticker]['roll_max_vol'] = ohlc_dic[ticker]['Volume'].rolling(20).max()
    ohlc_dic[ticker].dropna(inplace=True)
    tickers_signal[ticker] = ''
    tickers_ret[ticker] = []
    
for ticker in tickers:
    for i in range(len(ohlc_dic[ticker])):
        if tickers_signal[ticker] == '':
            tickers_ret[ticker].append(0)
            if (ohlc_dic[ticker]['High'][i] >= ohlc_dic[ticker]['roll_max_cp'][i] and \
                ohlc_dic[ticker]['Volume'][i] > 1.5*ohlc_dic[ticker]['roll_max_vol'][i-1]):
                tickers_signal[ticker] = 'Buy'
            elif (ohlc_dic[ticker]['Low'][i] <= ohlc_dic[ticker]['roll_min_cp'][i] and \
                ohlc_dic[ticker]['Volume'][i] > 1.5*ohlc_dic[ticker]['roll_max_vol'][i-1]):
                tickers_signal[ticker] = 'Sell'
        elif tickers_signal[ticker] == 'Buy':
            if ohlc_dic[ticker]['Low'][i] < (ohlc_dic[ticker]['Close'][i-1] - ohlc_dic[ticker]['ATR'][i-1]):
                tickers_signal[ticker] = ''
                tickers_ret[ticker].append((((ohlc_dic[ticker]['Close'][i-1] - ohlc_dic[ticker]['ATR'][i-1])/ohlc_dic[ticker]['Close'][i-1]) - 1))
            elif (ohlc_dic[ticker]['Low'][i] <= ohlc_dic[ticker]['roll_min_cp'][i] and \
                ohlc_dic[ticker]['Volume'][i] > 1.5*ohlc_dic[ticker]['roll_max_vol'][i-1]):
                tickers_signal[ticker] = 'Sell'
                tickers_ret[ticker].append((ohlc_dic[ticker]['Close'][i]/ohlc_dic[ticker]['Close'][i-1]) - 1)
            else:
                tickers_ret[ticker].append((ohlc_dic[ticker]['Close'][i]/ohlc_dic[ticker]['Close'][i-1]) - 1)
        elif tickers_signal[ticker] == 'Sell':
            if ohlc_dic[ticker]['High'][i] > (ohlc_dic[ticker]['Close'][i-1] + ohlc_dic[ticker]['ATR'][i-1]):
                tickers_signal[ticker] = ''
                tickers_ret[ticker].append(((ohlc_dic[ticker]['Close'][i-1] + ohlc_dic[ticker]['ATR'][i-1])/ohlc_dic[ticker]['Close'][i-1]) - 1)
            elif (ohlc_dic[ticker]['High'][i] >= ohlc_dic[ticker]['roll_max_cp'][i] and \
                ohlc_dic[ticker]['Volume'][i] > 1.5*ohlc_dic[ticker]['roll_max_vol'][i-1]):
                tickers_signal[ticker] = 'Buy'
                tickers_ret[ticker].append((ohlc_dic[ticker]['Close'][i]/ohlc_dic[ticker]['Close'][i-1]) - 1)
            else:
                tickers_ret[ticker].append((ohlc_dic[ticker]['Close'][i]/ohlc_dic[ticker]['Close'][i-1]) - 1)
    ohlc_dic[ticker]['ret'] = np.array(tickers_ret[ticker])
               
# Calculate overall strategy's KPI

strategy_df = pd.DataFrame()
for ticker in tickers:
    strategy_df[ticker] = ohlc_dic[ticker]['ret']              
strategy_df['ret'] = strategy_df.mean(axis=1)
CAGR(strategy_df)
sharpe(strategy_df, .05)
max_dd(strategy_df)    

