#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Th Oct 29 13:33:12 2017

@author: rweegenaar

This script goes long and short on minima and maxima of the Moving Average
"""

import pandas as pd
import numpy as np
import glob

# Set Moving Average Period

Period = 100

# Read CSVs
file_names = glob.glob('*.csv')
name1 = file_names[0]

# dataframe1
df1 = pd.read_csv(name1, header=None, names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

A1 = df1['date'] + " " + df1['time']

D1 = list(set(A1))
D1_date = pd.to_datetime(D1)
D1_date.values.sort()
# i = D1_date.size

A1 = pd.to_datetime(A1)

# create new dataframe 'df2' with DateTimes and Moving Averages
# preallocate column with zeros
MA = np.zeros(A1.size)
deltaMA = np.zeros(A1.size)
POS = np.zeros(A1.size)
df2 = pd.DataFrame(A1)
df2['close'] = df1['close']
df2['MA'] = MA

# Calculate and store Moving Average with length 'Period' (value given at top script)

i = Period
k = A1.size - i + 1

for p in range(k):
        closesum = 0
        for j in range(i):

            closesum = closesum + df1.close[j+p]

        closeavg = closesum/i

        # store moving average value in df2
        df2.at[p+i-1, 'MA'] = closeavg
        # determine sign of delta MA
        if df2.MA[p+i-1] - df2.MA[p+i-2] >= 0:
            df2.at[p+i-1, 'deltaMA'] = 1
        else:
            df2.at[p+i-1, 'deltaMA'] = -1

        #identify minimum (LONG Position)
        if df2.deltaMA[p+i-1] > 0 and df2.deltaMA[p+i-2] > 0 and df2.deltaMA[p+i-3] > 0 and \
            df2.deltaMA[p+i-4] < 0 and df2.deltaMA[p+i-5] < 0 and df2.deltaMA[p+i-6] < 0:
            df2.at[p+i-1, 'POS'] = 1
        #identify maximum (Short Position)
        elif df2.deltaMA[p+i-1] < 0 and df2.deltaMA[p+i-2] < 0 and df2.deltaMA[p+i-3] < 0 and \
                df2.deltaMA[p+i-4] > 0 and df2.deltaMA[p+i-5] > 0 and df2.deltaMA[p+i-6] > 0:
            df2.at[p+i-1, 'POS'] = -1
        else:
            df2.at[p+i-1, 'POS'] = np.NaN

print(df2)






# Plot Lagindex and price
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column

PlotDates = A1.iloc[i:]
PlotClose = df2.close.iloc[i:]
PlotMA = df2.MA.iloc[i:]

output_file("MovingAverage.html")
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover,crosshair"
Title = 'Moving Average; Period = ' + str(Period)
# plot 1 - Close Prices & Moving Average
p1 = figure(plot_width=1050, plot_height=600, x_axis_type='datetime',
            tools=TOOLS, title=Title)
p1.line(PlotDates, PlotClose, line_width=0.8, color='firebrick')
p1.line(PlotDates, PlotMA, line_width=2, color='navy')


#TODO adjust following code

# # plot positions
# # redefine Position for graphics
# # Convert 'Position' to entry prices for Long & Short Positions
# PositionPlotLong = np.clip(Position,0,1)
# PositionPlotLong[PositionPlotLong == 0] = np.nan
# PositionPlotLong = PositionPlotLong*PlotPriceClose
#
# PositionPlotShort = np.clip(Position,-1,0)
# PositionPlotShort[PositionPlotShort == 0] = np.nan
# PositionPlotShort = -PositionPlotShort*PlotPriceClose
#
# p1.triangle(PlotDates, PositionPlotLong, size=15,
#               line_color="black", fill_color="lime", alpha=0.8)
# p1.inverted_triangle(PlotDates, PositionPlotShort, size=15,
#               line_color="black", fill_color="red", alpha=0.7)

show(p1)


