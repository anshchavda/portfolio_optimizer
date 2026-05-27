# Portfolio Optimizer
A Python-based portfolio optimization tool that uses historical stock return data from Yahoo Finance to estimate optimal tangency portfolio weights using mean-variance analysis.


## The program:

- Pulls historical stock price data from Yahoo Finance (`yfinance`)
- Calculates annualized historical returns
- Builds an annualized covariance matrix
- Uses the 10-Year Treasury Yield as a proxy for the risk-free rate
- Computes tangency portfolio weights
- Estimates expected return, volatility, and Sharpe ratio
- Suggests dollar allocations based on a user-input investment amount

## Example output:

 Final Portfolio Metrics:

 Expected Annual Return: 18.73%
 Expected Annual Volatility: 20.51%
 Sharpe Ratio: 0.69
 Risk-Free Rate: 4.49%


For the optimal risk-return tradeoff, you should invest:

 16.28% of your portfolio in BA [Buy $1628.00 of BA]
 27.34% of your portfolio in LMT [Buy $2734.00 of LMT]
 56.38% of your portfolio in NOC [Buy $5638.00 of NOC]


## Limitations

This project uses historical returns as a proxy for expected returns, meaning outputs are highly sensitive to the selected lookback period and recent market performance.

This project is intended for educational purposes and exploration of portfolio optimization concepts. This is NOT investment advice. 

## Future Improvements

Potential future enhancements include:

- Efficient frontier visualization
- Long-only optimization constraints
