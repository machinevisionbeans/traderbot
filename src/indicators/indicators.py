
from talib import MACDFIX, RSI, EMA, SAR, SMA, TRIX, BBANDS, CDLIDENTICAL3CROWS, CDL3BLACKCROWS, CDL3WHITESOLDIERS, CDLMORNINGSTAR, CDLEVENINGSTAR, CDL3LINESTRIKE, CDLMORNINGDOJISTAR, CDLEVENINGDOJISTAR, CDL3OUTSIDE, CDLENGULFING, CDLBELTHOLD, CDLABANDONEDBABY, CDL3INSIDE, CDLPIERCING, CDLDARKCLOUDCOVER, CDLBREAKAWAY,CDLXSIDEGAP3METHODS, CDLHAMMER, CDLSHOOTINGSTAR
import indicators.ATRcalc as atrcalc
import os

import pandas as pd
class Indicator:

    # indicatorlist = ['ichimoku200', 'macdRSI', 'parabolic200', 'SMA200']    
    def beginCalc(self, df, tickerName):
        ## FILL THIS IN AS MORE INDICATORS ARE ADDED
        indicatorlist = ['ichimoku200','macdRSI', 'macd200', 'parabolic200', 'SMA200', 'trix200', 'macdTRIX', 'bbands200']

        # Step 1: Find out if analysis csv exists
        
        if not os.path.exists('./database/' + tickerName + '/IndicatorScore.csv'):
            columnNames = indicatorlist
            frame = pd.DataFrame(columns=columnNames)
            frame.loc[len(frame)] = 100
            frame.to_csv('./database/' + tickerName + '/IndicatorScore.csv')
        else:
            columnCheck = pd.read_csv('./database/' + tickerName + '/IndicatorScore.csv', index_col=0)
            for i in indicatorlist:
                if not i in columnCheck.columns:
                    avg = columnCheck.mean(axis = 1)
                    columnCheck.insert(len(columnCheck.columns), i, avg)
            columnCheck.to_csv('./database/' + tickerName + '/IndicatorScore.csv')
        resultsDict = {}

        for i in indicatorlist:
            fnRun = getattr(self, i)
            position, amount, currentclose, stoploss, takeprofit, confidence = fnRun(df)
            indivResult = {"position":position, "amount":amount, "entry":currentclose, "stoploss":stoploss, "takeprofit":takeprofit, "confidence":confidence}
            resultsDict[i] = indivResult
            
        return resultsDict
    
    def ichimoku200(self,df):
        ## Step 1: 
        #####PLACEHOLDER
        # df = pd.read_csv('./database/TSLA/temp2.csv')
        #####END_PLACEHOLDER
        df = df.dropna()
        ###1. Getting Parameters

        ##a. Senkou Span B Ahead
        Currentfifty_two = df.head(52)
        Currentfifty_two_high = Currentfifty_two['high'].max()
        Currentfifty_two_low = Currentfifty_two['low'].min()
        AheadSenkouB = (Currentfifty_two_high + Currentfifty_two_low) / 2
        # print("SenkouBAhead\n", AheadSenkouB)

        ##b. Current Kijun-Sen
        Currenttwenty_six = Currentfifty_two.head(26)
        Currenttwenty_six_high = Currenttwenty_six['high'].max()
        Currenttwenty_six_low = Currenttwenty_six['low'].min()
        CurrentKijun = (Currenttwenty_six_high + Currenttwenty_six_low) / 2
        # print("Kijun-Sen\n" , CurrentKijun)

        ##c. Current Tenkan-Sen
        Currentnine = Currenttwenty_six.head(9)
        Currentnine_high = Currentnine['high'].max()
        Currentnine_low = Currentnine['low'].min()
        CurrentTenkan = (Currentnine_high + Currentnine_low)/2

        # print("Tenkan-Sen\n", CurrentTenkan)

        ##d. Senkou Span A Ahead
        AheadSenkouA = (CurrentKijun + CurrentTenkan) / 2
        # print("SenkouAAhead\n", AheadSenkouA)

        ##e. Senkou Span B Current
        Pastfifty_two = df.iloc[26:].head(52)
        Pastfifty_two_high = Pastfifty_two['high'].max()
        Pastfifty_two_low = Pastfifty_two['low'].min()
        CurrentSenkouB = (Pastfifty_two_high + Pastfifty_two_low) / 2
        # print("SenkouBCurrent\n", CurrentSenkouB)

        ##f. Past Kijun-Sen
        Pasttwenty_six = Pastfifty_two.head(26)
        Pasttwenty_six_high = Pasttwenty_six['high'].max()
        Pasttwenty_six_low = Pasttwenty_six['low'].min()
        PastKijun = (Pasttwenty_six_low + Pasttwenty_six_high) / 2
        # print("PastKijun-Sen\n",PastKijun)

        ##g. Past Tenkan-Sen
        Pastnine = Pasttwenty_six.head(9)
        Pastnine_high = Pastnine['high'].max()
        Pastnine_low = Pastnine['low'].min()
        PastTenkan = (Pastnine_high + Pastnine_low) / 2
        # print("PastTenkan-Sen\n", PastTenkan)

        ##h. Senkou Span A Current
        CurrentSenkouA = (PastKijun + PastTenkan) / 2
        # print("SenkouACurrent\n", CurrentSenkouA)

        ##i. Senkou Span B Past
        PastPastfifty_two = df.iloc[52:].head(52)
        PastPastfifty_two_high = PastPastfifty_two['high'].max()
        PastPastfifty_two_low = PastPastfifty_two['low'].min()
        PastSenkouB = (PastPastfifty_two_high + PastPastfifty_two_low) / 2

        ##j. Past Past Kijun - Sen
        PastPasttwenty_six = PastPastfifty_two.head(26)
        PastPasttwenty_six_high = PastPasttwenty_six['high'].max()
        PastPasttwenty_six_low = PastPasttwenty_six['low'].min()
        PastPastKijun = (PastPasttwenty_six_low + PastPasttwenty_six_high) / 2

        ##k. Past Past Tenkan-Sen
        PastPastnine = PastPasttwenty_six.head(9)
        PastPastnine_high = PastPastnine['high'].max()
        PastPastnine_low = PastPastnine['low'].min()
        PastPastTenkan = (PastPastnine_high + PastPastnine_low) / 2

        ##l. Senkou Span A Past
        PastSenkouA = (PastPastKijun + PastPastTenkan) / 2

        ##m. 200EMA
        emaInput = df.head(200)
        emaInput = emaInput.iloc[::-1]
        EMAclose = emaInput['close'].values
        ema = EMA(EMAclose, timeperiod=200)
        # print("EMA\n", ema[-1])

        ##n. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        priceclose = priceaction['close'].values[0]
        ### IMPT CHIKOU SPAN = PRICE CLOSE

        # print("pricehigh\n", pricehigh)
        # print("pricelow\n", pricelow)

        ### 2. Analysing using Data Provided
        ##tenkan-kijun crossover type
            ## -1 means negative crossover
            ## 1 means positive crossover
            ## 0 means both

        delayOnePeriod = df.iloc[1:]

        ##b. Current Kijun-Sen
        Delaytwenty_six = delayOnePeriod.head(26)
        Delaytwenty_six_high = Delaytwenty_six['high'].max()
        Delaytwenty_six_low = Delaytwenty_six['low'].min()
        DelayKijun = (Delaytwenty_six_high + Delaytwenty_six_low) / 2
        # print("Delay Kijun-Sen\n" , DelayKijun)

        ##c. Current Tenkan-Sen
        Delaynine = Delaytwenty_six.head(9)
        Delaynine_high = Delaynine['high'].max()
        Delaynine_low = Delaynine['low'].min()
        DelayTenkan = (Delaynine_high + Delaynine_low)/2

        # print("Tenkan-Sen\n", DelayTenkan)

        if DelayTenkan <= DelayKijun and CurrentTenkan >= CurrentKijun and pricelow > CurrentTenkan:
            crossover = 1
        elif DelayTenkan >= DelayKijun and CurrentTenkan <= CurrentKijun and pricehigh < CurrentTenkan:
            crossover = -1

        else: crossover = 0

        ##ahead cloud colour
            ## -1 means red cloud
            ## 1 means green cloud
            ## 0 means both

        if AheadSenkouA > AheadSenkouB: AheadCloud = 1
        elif AheadSenkouA < AheadSenkouB: AheadCloud = -1
        else: AheadCloud = 0

        ##market-ema type
            ## 1 means low > 200EMA
            ## -1 means high < 200EMA
            ## 0 means otherwise

        if pricelow > ema[-1]: marketEMA = 1
        elif pricehigh < ema[-1]: marketEMA = -1
        else: marketEMA = 0

        ##market-cloud type
            ## 1 means close is above current cloud, and close (lagging span) above the past cloud too
            ## -1 means close is below current cloud, and close (lagging span) below the past cloud too
            ## 0 means otherwise (absolutely no trading)

        if  pricelow > max(CurrentSenkouA,CurrentSenkouB) and pricelow > max(PastSenkouB,PastSenkouA):
            marketCloud = 1
        elif pricehigh < min(CurrentSenkouB, CurrentSenkouA) and pricehigh < min(PastSenkouA, PastSenkouB):
            marketCloud = -1
        else: marketCloud = 0



        if marketCloud == 1 and marketEMA > 0 and AheadCloud >= 0 and crossover > 0:
            position = 1 ##long
        elif marketCloud == -1 and marketEMA < 0 and AheadCloud <= 0 and crossover < 0:
            position = -1 ##short
        else: position = 0 ## no position
        amount = 50
        if position == 1:
            closeKijunDistance = priceclose - CurrentKijun
            adjustedDistance = 1.05 * closeKijunDistance
            stoploss = priceclose - adjustedDistance
            # amount = priceclose / (priceclose-stoploss)
            takeprofit = priceclose + 1.45*(priceclose - stoploss)
            if (takeprofit - priceclose) * amount < 0.1:
                amount = 0
                position = 0
                stoploss = 0
                takeprofit = 0

        elif position == -1:
            closeKijunDistance = CurrentKijun - priceclose
            adjustedDistance = 1.05 * closeKijunDistance
            stoploss = priceclose + adjustedDistance
            # amount = priceclose / (stoploss - priceclose)
            takeprofit = priceclose - 1.45*(stoploss - priceclose)
            if(priceclose - takeprofit) * amount < 0.1:
                amount = 0
                position = 0
                stoploss = 0
                takeprofit = 0
        else: 
            amount = 0
            stoploss = 0
            takeprofit = 0

        # ##FOR TEST
        # position = 1
        return [position, amount, priceclose, stoploss, takeprofit, 1]

    def macdRSI(self,df):
        #1. Calculate ATR for potential trade
        atr = atrcalc.ATRcalc(df)
        #####PLACEHOLDER
        # df = pd.read_csv('./database/AAPL.csv')
        #####END_PLACEHOLDER
        df = df.dropna()

        ###1. Getting Parameters
        ##a. RSI
        rsiInput = df.head(15)
        rsiInput = rsiInput.iloc[::-1]
        RSIclose = rsiInput['close'].values
        rsi = RSI(RSIclose,timeperiod=14)
        # print("RSI\n", rsi[-1])

        ##b. MACD
        macdInput = df.head(34)
        macdInput = macdInput.iloc[::-1]
        MACDclose = macdInput['close'].values
        macd, macdsignal, macdhist = MACDFIX(MACDclose, signalperiod = 9)
        # print("MACD\n", macd[-1])
        # print("Signal\n", macdsignal[-1])

        ##c. DelayedMACD
        delayedmacdInput = df.iloc[1:].head(34)
        delayedmacdInput = delayedmacdInput.iloc[::-1]
        delayedMACDclose = delayedmacdInput['close'].values
        delayedmacd, delayedmacdsignal, delayedmacdhist = MACDFIX(delayedMACDclose, signalperiod = 9)


        ##d. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        priceclose = priceaction['close'].values[0]
        # print("pricehigh\n", pricehigh)
        # print("pricelow\n", pricelow)

        ###2. Analysing using the data provided

        ##macd-signal crossover type
        ## -1 means negative crossover
        ## 1 means positive crossover
        ## 0 means both
        if delayedmacd[-1] < delayedmacdsignal[-1] and macd[-1] > macdsignal[-1]: crossover = 1
        elif delayedmacd[-1] > delayedmacdsignal[-1] and macd[-1] < macdsignal[-1]: crossover = -1
        else: crossover = 0

        ##OUTPUT
        if crossover > 0 and rsi[-1] <= 50 and macd[-1] < 0: position = 1
        elif crossover < 0 and rsi[-1] >= 50 and macd[-1] > 0: position = -1
        else: position = 0

        amount = 50
        if position == 1:
            stoploss = priceclose - 1.05 * atr
            takeprofit = priceclose + 1.45 * atr
            # amount = priceclose / (priceclose - stoploss)
            if (priceclose - stoploss) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0

        elif position == -1:
            stoploss = priceclose + 1.05*atr
            takeprofit = priceclose - 1.45 * atr
            # amount = priceclose / (stoploss - priceclose)
            if(stoploss - priceclose) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        else:
            stoploss = 0
            takeprofit = 0
            amount = 0

        ##For test
        # position = 1

        return [position, amount, priceclose, stoploss, takeprofit, 1]

    def parabolic200(self,df):
        df = df.dropna()

        ###1. Getting Parameters
        ##a. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        priceclose = priceaction['close'].values[0]
        ##b. SAR current

        sarCurrentInput = df.head(2)
        sarCurrentInput = sarCurrentInput.iloc[::-1]
        sarCurrentInputHigh = sarCurrentInput['high'].values
        sarCurrentInputLow = sarCurrentInput['low'].values
        sarCurrent = SAR(sarCurrentInputHigh, sarCurrentInputLow, acceleration = 0, maximum = 0)

        ##c. previous price action
        prevaction = df.iloc[1:].head(1)
        prevhigh = prevaction['high'].values[0]
        prevlow = prevaction['low'].values[0]
        prevclose = prevaction['close'].values[0]

        ##d. previous SAR
        sarPreviousInput = df.iloc[1:].head(2)
        sarPreviousInput = sarPreviousInput.iloc[::-1]
        sarPreviousInputHigh = sarPreviousInput['high'].values
        sarPreviousInputLow = sarPreviousInput['low'].values
        sarPrevious = SAR(sarPreviousInputHigh, sarPreviousInputLow, acceleration = 0, maximum = 0)

        ##b. 200EMA
        emaInput = df.head(200)
        emaInput = emaInput.iloc[::-1]
        EMAclose = emaInput['close'].values
        ema = EMA(EMAclose, timeperiod=200)

        ## SAR reversal
        ## 1 if from -ve become +ve
        ## -1 if from +ve become -ve
        ## 0 otherwise

        if prevclose < sarPrevious[-1] and priceclose > sarCurrent[-1]:
            change = 1
        elif prevclose > sarPrevious[-1] and priceclose < sarCurrent[-1]:
            change = -1
        else: change = 0

        ## 200EMA filtering false signal
        if pricelow > ema[-1]: marketEMA = 1
        elif pricehigh < ema[-1]: marketEMA = -1
        else: marketEMA = 0

        ##OUTPUT
        if marketEMA == 1 and change == 1 : position = 1
        elif marketEMA == -1 and change == -1: position = -1
        else: position = 0

        amount = 50

        if position == 1:
            stoploss = sarCurrent[-1]
            takeprofit = priceclose + 1.45*(priceclose - sarCurrent[-1])
            # amount = priceclose / (priceclose - stoploss)
            if(priceclose - stoploss) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        elif position == -1:
            stoploss = sarCurrent[-1]
            takeprofit = priceclose - 1.45 * (sarCurrent[-1] - priceclose)
            # amount = priceclose / (stoploss - priceclose)
            if(stoploss - priceclose) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        else:
            stoploss = 0
            takeprofit = 0
            amount = 0

        ##For test
        # position = 1

        return [position, amount, priceclose, stoploss, takeprofit, 1]

    def SMA200(self,df):
        df = df.dropna()

        ###1. Getting Parameters
        ##a. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        priceclose = priceaction['close'].values[0]

        ##b. previous price action
        prevaction = df.iloc[1:].head(1)
        prevhigh = prevaction['high'].values[0]
        prevlow = prevaction['low'].values[0]
        prevclose = prevaction['close'].values[0]

        ##d. current SMAs
        smaCurrentInput = df.head(20)
        sma20Current = SMA(smaCurrentInput['close'].values, timeperiod=20)
        smaCurrentInput = smaCurrentInput.head(10)
        sma10Current = SMA(smaCurrentInput['close'].values, timeperiod=10)

        ##e. previous SMAs
        smaPreviousInput = df.iloc[1:].head(20)
        sma20Previous = SMA(smaPreviousInput['close'].values, timeperiod=20)
        smaPreviousInput = smaPreviousInput.head(10)
        sma10Previous = SMA(smaPreviousInput['close'].values,timeperiod=10)

        ##f. 200EMA
        emaInput = df.head(200)
        emaInput = emaInput.iloc[::-1]
        EMAclose = emaInput['close'].values
        ema = EMA(EMAclose, timeperiod=200)

        ##trade conditions

        if sma10Previous[-1] < sma20Previous[-1] and sma10Current[-1] > sma20Current[-1]:
            crossover = 1
        elif sma10Previous[-1] > sma20Previous[-1] and sma10Current[-1] < sma20Current[-1]:
            crossover = -1
        else: crossover = 0

        ## 200EMA filtering false signal
        if pricelow > ema[-1]: marketEMA = 1
        elif pricehigh < ema[-1]: marketEMA = -1
        else: marketEMA = 0

        if crossover == 1 and marketEMA == 1:
            position = 1
        elif crossover == -1 and marketEMA == -1:
            position = -1
        else: position = 0

        atr = atrcalc.ATRcalc(df)
        amount = 50
        if position == 1:
            stoploss = priceclose - 1.05 * atr
            takeprofit = priceclose + 1.45 * atr
            # amount = priceclose / (priceclose - stoploss)
            if(priceclose- stoploss) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        elif position == -1:
            stoploss = priceclose + 1.05*atr
            takeprofit = priceclose - 1.45 * atr
            # amount = priceclose / (stoploss - priceclose)
            if(stoploss - priceclose) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        else:
            stoploss = 0
            takeprofit = 0
            amount = 0

        return [position, amount, priceclose, stoploss, takeprofit, 1]

    def macd200(self,df):
        #1. Calculate ATR for potential trade
        atr = atrcalc.ATRcalc(df)
        #####PLACEHOLDER
        # df = pd.read_csv('./database/AAPL.csv')
        #####END_PLACEHOLDER
        df = df.dropna()

        ###1. Getting Parameters
        

        ##b. MACD
        macdInput = df.head(34)
        macdInput = macdInput.iloc[::-1]
        MACDclose = macdInput['close'].values
        macd, macdsignal, macdhist = MACDFIX(MACDclose, signalperiod = 9)
        # print("MACD\n", macd[-1])
        # print("Signal\n", macdsignal[-1])

        ##c. DelayedMACD
        delayedmacdInput = df.iloc[1:].head(34)
        delayedmacdInput = delayedmacdInput.iloc[::-1]
        delayedMACDclose = delayedmacdInput['close'].values
        delayedmacd, delayedmacdsignal, delayedmacdhist = MACDFIX(delayedMACDclose, signalperiod = 9)

        ##c. 200EMA
        emaInput = df.head(200)
        emaInput = emaInput.iloc[::-1]
        EMAclose = emaInput['close'].values
        ema = EMA(EMAclose, timeperiod=200)

        # print("EMA\n", ema[-1])

        ##d. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        priceclose = priceaction['close'].values[0]
        # print("pricehigh\n", pricehigh)
        # print("pricelow\n", pricelow)

        ###2. Analysing using the data provided

        ##macd-signal crossover type
        ## -1 means negative crossover
        ## 1 means positive crossover
        ## 0 means both
        if delayedmacd[-1] < delayedmacdsignal[-1] and macd[-1] > macdsignal[-1]: crossover = 1
        elif delayedmacd[-1] > delayedmacdsignal[-1] and macd[-1] < macdsignal[-1]: crossover = -1
        else: crossover = 0
        ##market-ema type
        ## 1 means low > 200EMA
        ## -1 means high < 200EMA
        ## 0 means otherwise

        if pricelow > ema[-1]: marketEMA = 1
        elif pricehigh < ema[-1]: marketEMA = -1
        else: marketEMA = 0

        ##OUTPUT
        if marketEMA == 1 and crossover > 0  and macd[-1] < 0: position = 1
        elif marketEMA == -1 and crossover < 0  and macd[-1] > 0: position = -1
        else: position = 0
        amount = 50
        if position == 1:
            stoploss = priceclose - 1.05 * atr
            takeprofit = priceclose + 1.45 * atr
            # amount = priceclose / (priceclose - stoploss)
            if(priceclose - stoploss) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        elif position == -1:
            stoploss = priceclose + 1.05*atr
            takeprofit = priceclose - 1.45 * atr
            # amount = priceclose / (stoploss - priceclose)
            if(stoploss - priceclose) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        else:
            stoploss = 0
            takeprofit = 0
            amount = 0

        ##For test
        # position = 1

        return [position, amount, priceclose, stoploss, takeprofit, 1]

    def trix200(self,df):
        df = df.dropna()

        #1. Calculate ATR for potential trade
        atr = atrcalc.ATRcalc(df)

        trixInput = df.head(60)
        trixInput = trixInput.iloc[::-1]
        trixOutput = TRIX(trixInput['close'].values, timeperiod = 14)

        ##c. 200EMA
        emaInput = df.head(200)
        emaInput = emaInput.iloc[::-1]
        EMAclose = emaInput['close'].values
        ema = EMA(EMAclose, timeperiod=200)

        # print("EMA\n", ema[-1])

        ##d. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        priceclose = priceaction['close'].values[0]
        # print("pricehigh\n", pricehigh)
        # print("pricelow\n", pricelow)

        if trixOutput[-2] < 0 and trixOutput[-1] > 0:
            crossover = 1
        elif trixOutput[-2] > 0 and trixOutput[-1] < 0:
            crossover = -1
        else: crossover = 0


        if pricelow > ema[-1]: marketEMA = 1
        elif pricehigh < ema[-1]: marketEMA = -1
        else: marketEMA = 0

        ##OUTPUT
        if marketEMA == 1 and crossover > 0: position = 1
        elif marketEMA == -1 and crossover < 0: position = -1
        else: position = 0
        amount = 50
        if position == 1:
            stoploss = priceclose - 1.05 * atr
            takeprofit = priceclose + 1.45 * atr
            # amount = priceclose / (priceclose - stoploss)
            if(priceclose - stoploss) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        elif position == -1:
            stoploss = priceclose + 1.05*atr
            takeprofit = priceclose - 1.45 * atr
            # amount = priceclose / (stoploss - priceclose)
            if(stoploss - priceclose) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        else:
            stoploss = 0
            takeprofit = 0
            amount = 0
        
        return [position, amount, priceclose, stoploss, takeprofit, 1]

    def macdTRIX(self,df):
        df = df.dropna()
        #1. Calculate ATR for potential trade
        atr = atrcalc.ATRcalc(df)

        ##b. MACD
        macdInput = df.head(34)
        macdInput = macdInput.iloc[::-1]
        MACDclose = macdInput['close'].values
        macd, macdsignal, macdhist = MACDFIX(MACDclose, signalperiod = 9)
        # print("MACD\n", macd[-1])
        # print("Signal\n", macdsignal[-1])

        ##c. DelayedMACD
        delayedmacdInput = df.iloc[1:].head(34)
        delayedmacdInput = delayedmacdInput.iloc[::-1]
        delayedMACDclose = delayedmacdInput['close'].values
        delayedmacd, delayedmacdsignal, delayedmacdhist = MACDFIX(delayedMACDclose, signalperiod = 9)

        trixInput = df.head(60)
        trixInput = df.iloc[::-1]
        trixOutput = TRIX(trixInput['close'].values, timeperiod = 20)


        # print("EMA\n", ema[-1])

        ##d. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        priceclose = priceaction['close'].values[0]
        # print("pricehigh\n", pricehigh)
        # print("pricelow\n", pricelow)

        if delayedmacd[-1] < delayedmacdsignal[-1] and macd[-1] > macdsignal[-1] and trixOutput[-1] < 0 : position = 1
        elif delayedmacd[-1] > delayedmacdsignal[-1] and macd[-1] < macdsignal[-1] and trixOutput[-1] > 0: position = -1
        else: position = 0
        amount = 50
        if position == 1:
            stoploss = priceclose - 1.05 * atr
            takeprofit = priceclose + 1.45 * atr
            # amount = priceclose / (priceclose - stoploss)
            if(priceclose - stoploss) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        elif position == -1:
            stoploss = priceclose + 1.05*atr
            takeprofit = priceclose - 1.45 * atr
            # amount = priceclose / (stoploss - priceclose)
            if(stoploss - priceclose) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
        else:
            stoploss = 0
            takeprofit = 0
            amount = 0

        ##For test
        # position = 1
        return [position, amount, priceclose, stoploss, takeprofit, 1]

    def bbands200(self,df):
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
        bband = df.head(21)
        bband = bband.iloc[1:]
        bband = bband.iloc[::-1]
        bbandInput = bband['close'].values
        upperband, middleband, lowerband = BBANDS(bbandInput, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

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
        amount = 50
        if position == 1:
            stoploss = priceclose - 1.05 * atr
            takeprofit = priceclose + 1.45 * atr
            # amount = priceclose / (priceclose - stoploss)
            if(stoploss - priceclose) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0
                
        elif position == -1:
            stoploss = priceclose + 1.05*atr
            takeprofit = priceclose - 1.45 * atr
            # amount = priceclose / (stoploss - priceclose)
            if(stoploss - priceclose) * amount < 0.1:
                position = 0
                amount = 0
                stoploss = 0
                takeprofit = 0

        else:
            stoploss = 0
            takeprofit = 0
            amount = 0

        return [position, amount, priceclose, stoploss, takeprofit, 1]