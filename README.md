# Portfolio Backtesting Tools

**Author**: Eric Kennedy

## trendFollowing.py uses a 10 Month Simple Moving Average

Calculate the difference in return for buy-and-hold vs trend following
where closes below an ETF's 10 month simple moving average will sell and go to cash.

This trend following approach outperformed the S&P 500 ETF SPY from 1998 through
the 2001 and 2008 recessions. However it has lagged buy-and-hold after 2019,
especially after the tax consequences of selling are taken into account.

The only major sector ETF where trend following is still outperforming is the
XLK Technology ETF. It has the largest S&P 500 sector weight so it could
make sense to use trend following for that portion of an equity portfolio.
