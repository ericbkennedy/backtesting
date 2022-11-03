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

Because the interest paid on cash has been near zero for most of the last 20 years,
it is assumed any interest received by the trend following approach will be
offset by additional commissions and short term capital gain taxes.

### Backtesting using existing SPY or sector CSV files

```
$ git clone https://github.com/ericbkennedy/backtesting.git
```

Move into the cloned directory and start a new Python 3 [virtual environment](https://docs.python.org/3/tutorial/venv.html). You should be using Python 3.6 or later.

Run it as follows and it will output the result without considering taxes on dividends or capital gains.

```
$ cd backtesting
$ python3 trendFollowing.py SPY
SPY buy and hold 497% vs 468% for trend following since 12/31/98
Trend following outperformed through 9/30/22

$ python3 trendFollowing.py XLK
XLK buy and hold 519% vs 745% for trend following since 12/31/98
Trend following outperformed through 10/31/22
```

trendFollowing.py will create a CSV output file showing the monthly return for both strategies by month (e.g. SPY-return.csv)

Add a 'taxable' argument to calculate the effect of taxes (15% for dividends and 20% for capital gains):

```
$ python3 trendFollowing.py SPY taxable
SPY buy and hold 467% vs 342% for trend following since 12/31/98
Trend following outperformed through 1/31/19

$ python3 trendFollowing.py XLK taxable
XLK buy and hold 498% vs 518% for trend following since 12/31/98
Trend following outperformed through 10/31/22
```

trendFollowing.py will create a CSV output file showing the post-tax monthly return for both strategies by month (e.g. SPY-return-taxable.csv)

### Download additional monthly data from AlphaVantage.co

Create a file .apikey.txt with your own key from [AlphaVantage.co](https://www.alphavantage.co/support/#api-key)

Download monthly data for another ETF or stock

```
$ python3 getData.py BRK-A
Output saved to BRK-A-monthly.csv

$ python3 trendFollowing.py BRK-A
BRK-A buy and hold 790% vs 238% for trend following since 1999-12-31
Trend following outperformed through 2009-02-27
```

For simplicity, getData.py will exit if it detects a stock split. AlphaVantage's API doesn't include a stock split column and the adjusted close column reflects both dividend adjustments and stock splits.

```
$ python3 getData.py BRK-B
A stock split may have occurred on 2009-12-31 because the adjusted close 65.7200 != historic 3286.0000
trendFollowing.py is only intended to backtest ETFs which do not have stock splits
```
