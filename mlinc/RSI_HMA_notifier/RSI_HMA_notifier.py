import quandl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

with open("C:\Data\\2_Personal\quandl_api.txt", 'r') as f:
    api_key = f.read()

file_robert = 'C:\Data\\2_Personal\Python_Projects\ifttt_info_robert.txt'

# This script returns the latest RSI and HMA values

RSI_period = 14
HMA_period = 10

# Commodity: Rough Rice
df1 = quandl.get('CHRIS/CME_RR1.6', start_date='2018-04-01', api_key=api_key)

# remove HMA period from start of df1
# df1 = df1[HMA_period-1:]

# SMA
def runningMeanFast(x, N):
    # return np.convolve(x, np.ones((N,)) / N)[(N - 1):]
    return np.convolve(x, np.ones((N,)) / N, mode='valid')
# SMA 0.5 period

# HMA


y = runningMeanFast(df1.Settle, HMA_period)
df1 = df1[HMA_period-1:]
y = pd.Series(y, index=df1.index)
# print(y)

df1['avg'] = y
print(df1)

print(df1.shape)
print(y.size)

fig, ax = plt.subplots()
ax.plot(df1.index, df1.Settle, df1.index, df1.avg)
plt.grid()
plt.show()


n = HMA_period

def trinum(n):
    # calculates the "triangular number" of a number
    # https://www.mathsisfun.com/algebra/triangular-numbers.html

    return n * (n + 1) / 2

def wma(values, window):
    # requires trinum.py

    # using definition provided at
    # http://www.oanda.com/forex-trading/learn/forex-indicators/weighted-moving-average

    # create an array of weights
    # use floats when creating array, or the result is integer division below
    # and, note that they are reversed.  why?  read this:
    # http://stackoverflow.com/questions/12816011/weighted-moving-average-with-numpy-convolve
    weights = np.arange(window, 0, -1.0)
    weights /= trinum(window)

    # created wma array with NaN values for indexes < window value
    weighted_moving_averages = np.empty(window - 1)
    weighted_moving_averages[:] = np.NAN

    # then append the wma's onto the end
    weighted_moving_averages = np.append(weighted_moving_averages, np.convolve(values, weights, 'valid'))

    return weighted_moving_averages

def hma(values, window):
    # requires wma.py

    # HMA = WMA(2*WMA(PRICE, N/2) - WMA(PRICE, N), SQRT(N))

    period = int(np.sqrt(window))

    # created wma array with NaN values for indexes < window value
    # hull_moving_averages = np.empty(window)
    # hull_moving_averages[:] = np.NAN

    wma1 = 2 * wma(values, window / 2)
    wma2 = wma(values, window)

    hull_moving_averages = wma((wma1 - wma2), period)

    return hull_moving_averages

