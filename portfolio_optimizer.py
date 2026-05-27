# Mean-Variance Portfolio Optimizer
# Pulls historical stock data from Yahoo Finance, estimates annualized returns
# and covariance, and calculates tangency portfolio weights.
# Author: Ansh Chavda

import numpy as np
import pandas as pd
import yfinance as yf

# asks user how many stocks to include
print("\n----Welcome to the Tangency Portfolio Weightage Calculator----\n\n")
print("First, enter the quantity of stocks you'd like weighed out:")

while True:
    try:
        stockcount = int(input("Number of Stocks (greater than 2): "))
        if stockcount <= 2:
            print("\nInvalid input. Please enter a number greater than 2.\n")
            continue
        break
    except ValueError:
        print("\nInvalid input. Please enter a whole number.\n")

stocklist = []



print("\n\nNow, enter each stock ticker:")

# collects ticker symbols, standardizes to uppercase, and stores them in a list
for i in range(stockcount):
    stock = input("Stock Ticker " + str((i+1)) + ": ").upper()
    stocklist.append(stock)

# gathers dollar value of the user portfolio

while True:
    try:
        dollars = float(input("\nFinally, input your investment amount in USD: "))
        break
    except ValueError:
        print("\nInvalid input. Please enter a valid number.\n")







print("\n\nLoading ...\n\n")
# sorts tickers so output weights match the downloaded yfinance column order
stocklist.sort()
yfdata = yf.download(stocklist, period='1y', interval='1d')["Close"]

# Remove tickers with failed or missing data
yfdata = yfdata.dropna(axis=1, how="all")

# Update stocklist to only include successfully downloaded tickers
stocklist = list(yfdata.columns)
stockcount = len(stocklist)

if stockcount < 2:
    raise ValueError("Not enough valid tickers downloaded.")

dailyreturns = yfdata.pct_change().dropna()

if dailyreturns.empty:
    raise ValueError("No valid return data. Try a longer period or fewer tickers.")

# calculates annualized historical mean returns from daily percentage returns
annualizedreturn = (dailyreturns.mean() * 252)
returns = np.array(annualizedreturn)

# pulls the 10-year Treasury yield as rf rate
rf = np.array((yf.download(tickers="^TNX", period= '1mo')["Close"]).tail(1))
rf = float(rf[0][0]/100)

# prepares inputs for mean variance optimization
excessreturns = returns - rf
covarmatrix = (dailyreturns.cov() * 252)
inversematrix = np.linalg.inv(covarmatrix)
ones = np.ones(stockcount)

# calculates tangency portfolio weights, return, variance, volatility, and minimum variance weights
tangencyweights = (inversematrix @ excessreturns) / (ones @ inversematrix @ excessreturns)
tangencyportfolioreturn = tangencyweights.T @ returns
variance = tangencyweights.T @ covarmatrix @ tangencyweights
stdev = np.sqrt(variance)
minvarweights = (inversematrix @ ones.T) / (ones @ inversematrix @ ones.T)
sharpe = (tangencyportfolioreturn - rf) / stdev

expectedannualreturn = round(tangencyportfolioreturn*100, 2)
expectedannualvolatility = round(stdev*100, 2)

print("\nFinal Portfolio Metrics:\n")
print("Expected Annual Return: " + str(expectedannualreturn) + "%")
print("Expected Annual Volatility: " + str(expectedannualvolatility) + "%")
print("Sharpe Ratio: " + str(round(sharpe, 2)))
print("Risk-Free Rate: " + str(round(rf*100, 2)) + "%")


print("\n\nFor the optimal risk-return tradeoff, you should invest:\n")
# prints recommended tangency portfolio weights, including short positions if weights are negative
for i in range(stockcount):
    weight = round((float((tangencyweights[i])*100)),2)
    dollarweight = round(dollars*weight/100, 2)
    if weight >= 0:
        print(" " + str(weight) + "% of your portfolio in " + stocklist[i] + (" [Buy $" + str(dollarweight)) + " of " + stocklist[i] + "]")
    else:
        print(str(weight) + "% of your portfolio in " + stocklist[i] + " [Short $" + str(-dollarweight) + " of " + stocklist[i] + "]")
print("\n")