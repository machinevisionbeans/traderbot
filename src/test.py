import pandas as pd
from talib import MACDFIX, RSI, EMA, SAR, SMA, TRIX, BBANDS, CDLIDENTICAL3CROWS, CDL3BLACKCROWS, CDL3WHITESOLDIERS, CDLMORNINGSTAR, CDLEVENINGSTAR, CDL3LINESTRIKE, CDLMORNINGDOJISTAR, CDLEVENINGDOJISTAR, CDL3OUTSIDE, CDLENGULFING, CDLBELTHOLD, CDLABANDONEDBABY, CDL3INSIDE, CDLPIERCING, CDLDARKCLOUDCOVER, CDLBREAKAWAY,CDLXSIDEGAP3METHODS, CDLHAMMER, CDLSHOOTINGSTAR
import indicators.ATRcalc as atrcalc
import os
#1. Calculate ATR for potential trade
#####PLACEHOLDER
df = pd.read_csv('./database/AAPL/temp2.csv')
#####END_PLACEHOLDER
#1. Calculate ATR for potential trade
#####PLACEHOLDER
# df = pd.read_csv('./database/AAPL.csv')
#####END_PLACEHOLDER
df = df.dropna()

#1. Calculate ATR for potential trade
atr = atrcalc.ATRcalc(df)

## a. checkpatterns
cdlInput = df.head(20)
cdlInput = cdlInput.iloc[::-1]
aa = cdlInput['open'].values
ab = cdlInput['high'].values
ac = cdlInput['low'].values
ad = cdlInput['close'].values
outputI3C = CDLIDENTICAL3CROWS(aa,ab,ac,ad)
output3BC = CDL3BLACKCROWS(aa,ab,ac,ad)
output3WS = CDL3WHITESOLDIERS(aa,ab,ac,ad)
outputMS = CDLMORNINGSTAR(aa,ab,ac,ad)
outputES = CDLEVENINGSTAR(aa,ab,ac,ad)
output3LS = CDL3LINESTRIKE(aa,ab,ac,ad)
outputMDS = CDLMORNINGDOJISTAR(aa,ab,ac,ad)
outputEDS = CDLEVENINGDOJISTAR(aa,ab,ac,ad)
output3O = CDL3OUTSIDE(aa,ab,ac,ad)
outputE = CDLENGULFING(aa,ab,ac,ad)
outputBH = CDLBELTHOLD(aa,ab,ac,ad)
outputAB = CDLABANDONEDBABY(aa,ab,ac,ad)
output3I = CDL3INSIDE(aa,ab,ac,ad)
outputP = CDLPIERCING(aa,ab,ac,ad)
outputCDD = CDLDARKCLOUDCOVER(aa,ab,ac,ad)
outputB = CDLBREAKAWAY(aa,ab,ac,ad)
outputXSG3M = CDLXSIDEGAP3METHODS(aa,ab,ac,ad)
outputH = CDLHAMMER(aa,ab,ac,ad)
outputSS = CDLSHOOTINGSTAR(aa,ab,ac,ad)

if outputI3C[-1]>0 or output3BC[-1]>0 or output3WS[-1]>0 or outputMS[-1]>0 or outputES[-1]>0 or output3LS[-1]>0 or outputMDS[-1]>0 or outputEDS[-1]>0 or output3O[-1]>0 or outputE[-1]>0 or outputBH[-1]>0 or outputAB[-1]>0 or output3I[-1]>0 or outputP[-1]>0 or outputCDD[-1]>0 or outputB[-1]>0 or outputXSG3M[-1]>0 or outputH[-1]>0 or outputSS[-1]>0:
    pattern = 1
elif  outputI3C[-1]<0 or output3BC[-1]<0 or output3WS[-1]<0 or outputMS[-1]<0 or outputES[-1]<0 or output3LS[-1]<0 or outputMDS[-1]<0 or outputEDS[-1]<0 or output3O[-1]<0 or outputE[-1]<0 or outputBH[-1]<0 or outputAB[-1]<0 or output3I[-1]<0 or outputP[-1]<0 or outputCDD[-1]<0 or outputB[-1]<0 or outputXSG3M[-1]<0 or outputH[-1]<0 or outputSS[-1]<0:
    pattern = -1
else: pattern = 0

##b. get BBands
upperband, middleband, lowerband = BBANDS(ad, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

##c. 200EMA
emaInput = df.head(200)
emaInput = emaInput.iloc[::-1]
EMAclose = emaInput['close'].values
ema = EMA(EMAclose, timeperiod=200)

##d. current price action
priceaction = df.head(1)
pricehigh = priceaction['high'].values[0]
pricelow = priceaction['low'].values[0]
priceclose = priceaction['close'].values[0]

if pricehigh > upperband[-1]: breakBand = -1
elif pricelow < lowerband[-1]: breakBand = 1
else: breakBand = 0

if pricelow > ema[-1]: marketEMA = 1
elif pricehigh < ema[-1]: marketEMA = -1
else: marketEMA = 0

##OUTPUT
if marketEMA == 1 and pattern == 1 and breakBand == 1: position = 1
elif marketEMA == -1 and pattern == -1 and breakBand == -1: position = -1
else: position = 0

if position == 1:
    stoploss = priceclose - 1.05 * atr
    takeprofit = priceclose + 1.45 * atr
    amount = priceclose / (priceclose - stoploss)
elif position == -1:
    stoploss = priceclose + 1.05*atr
    takeprofit = priceclose - 1.45 * atr
    amount = priceclose / (stoploss - priceclose)
else:
    stoploss = 0
    takeprofit = 0
    amount = 0
##For test
# position = 1