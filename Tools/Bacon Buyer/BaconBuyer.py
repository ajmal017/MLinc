#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Th Oct 29 13:33:12 2017

@author: rweegenaar

This script goes long and short on minima and maxima of the Hull Moving Average
"""

import pandas as pd
import numpy as np
import glob
from bokeh.plotting import figure, output_file, show

# INPUT
# Set Moving Average Period
MAPeriod = 150
# Set Minimum Stop Loss (at least larger than spread)
MinSL = 0.002
# Risk Reward Ratio
RRR = 1

# Read CSVs
file_names = glob.glob('*.csv')
name1 = file_names[0]

# dataframe1
df1 = pd.read_csv(name1, header=None, names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

A1 = df1['date'] + " " + df1['time']

D1 = list(set(A1))
D1_date = pd.to_datetime(D1)
D1_date.values.sort()

A1 = pd.to_datetime(A1)

# create new dataframe 'df2' with DateTimes and Moving Averages
# preallocate columns with zeros
df2 = pd.DataFrame(A1)
DWMA = np.zeros(A1.size)
WMA = np.zeros(A1.size)
HMA = np.zeros(A1.size)
deltaWMA = np.zeros(A1.size)
dHMA = np.zeros(A1.size)
POS = np.zeros(A1.size)
SL = np.zeros(A1.size)
TP = np.zeros(A1.size)

df2['close'] = df1['close']
df2['low'] = df1['low']
df2['high'] = df1['high']
df2['DWMA'] = DWMA
df2['WMA'] = WMA
df2['HMA'] = HMA
df2['deltaWMA'] = deltaWMA
df2['dHMA'] = dHMA
df2['SL'] = SL
df2['TP'] = TP

# Periods for Hull Moving Average
# int(round()) rounds to nearest integer
i = int(round(0.5*MAPeriod))
q = MAPeriod
r = int(round(MAPeriod ** 0.5))

k = A1.size

# loop going forward in time
for p in range(q-1, k):
        # print progress
        print(A1[p])

        # 'Hull Moving Average'
        # https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/hull-moving-average
        # https://tradingsim.com/blog/hull-ma/
        # https://oxfordstrat.com/trading-strategies/hull-moving-average/

        # step (1)
        # calc 2x Weighted Moving Average (DWMA) with period i = integer(0.5*MAPeriod)
        sum1 = 0
        for j in range(q-i, q):

            sum1 = sum1 + (j-i+1)*df1.close[p+j-q+1]
        # ((i**2+i)/2) with i = 5: 5+4+3+2+1 = 15
        DWMA = 2*(sum1/((i**2+i)/2))
        df2.at[p, 'DWMA'] = DWMA

        # step (2)
        # calc Weighted Moving Average (WMA) with period q = MAPeriod
        # subtract WMA from DWMA
        sum2 = 0
        for j in range(q):

            sum2 = sum2 + (j+1)*df1.close[p+j-q+1]
        WMA = (sum2/((q**2+q)/2))
        df2.at[p, 'WMA'] = WMA
        deltaWMA = DWMA - WMA
        # store moving average value in df2
        df2.at[p, 'deltaWMA'] = deltaWMA

        # step (3)
        # calc Weighted Moving Average (WMA) with period r = integer(sqrt(MAPeriod))
        # from deltaWMA data to get the Hull Moving Average
        sum3 = 0
        for j in range(r):

            sum3 = sum3 + (j+1)*df2.deltaWMA[p+j-r+1]
        HMA = (sum3/((r**2+r)/2))
        df2.at[p, 'HMA'] = HMA

        # determine sign of delta HMA
        if df2.HMA[p] - df2.HMA[p-1] >= 0:
            df2.at[p, 'dHMA'] = 1
        else:
            df2.at[p, 'dHMA'] = -1

        # Place position (1 is Long, -1 is short)
        # identify minimum (LONG Position)
        if df2.dHMA[p] > 0 \
                and df2.dHMA[p - 1] < 0 \
                and df2.dHMA[p - 2] < 0 \
                and df2.dHMA[p - 3] < 0 \
                and df2.dHMA[p - 4] < 0 \
                and df2.dHMA[p - 5] < 0 \
                and df2.dHMA[p - 6] < 0:
            df2.at[p, 'POS'] = 1
            # determine Stop Loss Price
            if df2.close[p] - df2.HMA[p] > MinSL:
                df2.at[p, 'SL'] = df2.HMA[p]
            else:
                df2.at[p, 'SL'] = df2.close[p]-MinSL
            # determine Take Profit Price
            df2.at[p, 'TP'] = RRR * (df2.close[p] - df2.SL[p]) + df2.close[p]


        # identify maximum (Short Position)
        elif df2.dHMA[p] < 0 \
                and df2.dHMA[p - 1] > 0 \
                and df2.dHMA[p - 2] > 0 \
                and df2.dHMA[p - 3] > 0 \
                and df2.dHMA[p - 4] > 0 \
                and df2.dHMA[p - 5] > 0 \
                and df2.dHMA[p - 6] > 0:
            df2.at[p, 'POS'] = -1
            # determine Stop Loss Price
            if df2.HMA[p] - df2.close[p] > MinSL:
                df2.at[p, 'SL'] = df2.HMA[p]
            else:
                df2.at[p, 'SL'] = df2.close[p] + MinSL
            # determine Take Profit Price
            df2.at[p, 'TP'] = RRR * (df2.close[p] - df2.SL[p]) + df2.close[p]
        else:
            df2.at[p, 'POS'] = np.NaN
            df2.at[p, 'SL'] = np.NaN
            df2.at[p, 'TP'] = np.NaN

# print Dataframe
with pd.option_context('display.max_rows', None, 'display.max_columns', 10):
    print(df2)

# Plot HMA and price

# crop arrays to correct size
PlotDates = A1.iloc[q+r:]
PlotClose = df2.close.iloc[q+r:]
PlotHigh = df2.high.iloc[q+r:]
PlotLow = df2.low.iloc[q+r:]
PlotHMA = df2.HMA.iloc[q+r:]
PlotPOS = df2.POS.iloc[q+r:]
PlotSL = df2.SL.iloc[q+r:]
PlotTP = df2.TP.iloc[q+r:]

output_file("MovingAverage.html")
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover,crosshair"
Title = 'Bacon Buyer Hull Moving Average; Period = ' + str(MAPeriod) + '; ' + str(name1)
# plot 1 - Close Prices & Hull Moving Average
p1 = figure(plot_width=1050, plot_height=600, x_axis_type='datetime',
            tools=TOOLS, title=Title)
p1.line(PlotDates, PlotClose, line_width=0.8, color='firebrick')
p1.line(PlotDates, PlotLow, line_width=0.4, color='grey')
p1.line(PlotDates, PlotHigh, line_width=0.4, color='grey')
p1.line(PlotDates, PlotHMA, line_width=2, color='navy')

# plot positions
# redefine Position for graphics
# Convert 'Position' to entry prices for Long & Short Positions
PositionPlotLong = np.clip(PlotPOS, 0, 1)
PositionPlotLong[PositionPlotLong == 0] = np.nan
PositionPlotLong = PositionPlotLong*PlotClose

PositionPlotShort = np.clip(PlotPOS, -1, 0)
PositionPlotShort[PositionPlotShort == 0] = np.nan
PositionPlotShort = -PositionPlotShort*PlotClose

# Take Positions
p1.triangle(PlotDates, PositionPlotLong, size=15,
              line_color="black", fill_color="lime", alpha=0.8)
p1.inverted_triangle(PlotDates, PositionPlotShort, size=15,
              line_color="black", fill_color="red", alpha=0.7)

# SLs and TPs
p1.circle(PlotDates, PlotSL, size=10,
              line_color="red", fill_color="red", fill_alpha=0.2)
p1.circle(PlotDates, PlotTP, size=10,
              line_color="green", fill_color="green", fill_alpha=0.2)

show(p1)



