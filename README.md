# Portfolio Backtesting Tools

**Author**: Eric Kennedy

## trendFollowing.py uses a 10 Month Simple Moving Average

Calculate the difference in return for buy-and-hold vs trend following
where closes below an ETF's 10 month simple moving average will sell and go to cash.

This trend following approach outperformed the S&P 500 ETF SPY from 1998 through
the 2001 and 2008 recessions. However volatility at the end of 2018 and in 2020
led whipsaws of selling one month and repurchasing the following month at a higher price,
eroding the performance of the trend following strategy,
especially after the tax consequences of selling are taken into account.

The only major sector ETFs where trend following is still outperforming *after taxes* is the
XLK Technology ETF. It has the largest S&P 500 sector weight so it could
make sense to use trend following for that portion of an equity portfolio.

Because the interest paid on cash has been near zero for most of the last 20 years,
it is assumed any interest received by the trend following approach will be
offset by additional commissions and short term capital gain taxes.

### Backtesting using existing SPY or sector CSV files

```
# git clone https://github.com/ericbkennedy/backtesting.git
```

Move into the cloned directory use Python 3.6 or later to run the trendFollowing.py script.

Run it as follows and it will output the result without considering taxes on dividends or capital gains.

```
# cd backtesting
# python3 trendFollowing.py SPY
SPY buy and hold 495% vs 515% for trend following since 12/31/98
Trend following outperformed through 12/30/22

# python3 trendFollowing.py XLK
XLK buy and hold 506% vs 1040% for trend following since 12/31/98
Trend following outperformed through 12/30/22

# python3 trendFollowing.py XOP
XOP buy and hold 95% vs 223% for trend following since 7/31/06
Trend following outperformed through 12/30/22

# python3 trendFollowing.py XOP taxable
XOP buy and hold 94% vs 214% for trend following since 7/31/06
Trend following outperformed through 12/30/22
```

trendFollowing.py will create a CSV output file showing the monthly return for both strategies by month (e.g. SPY-return.csv)

Add a 'taxable' argument to calculate the effect of taxes (15% for dividends and 20% for capital gains):

```
# python3 trendFollowing.py SPY taxable
SPY buy and hold 464% vs 366% for trend following since 12/31/98
Trend following outperformed through 5/31/19

# python3 trendFollowing.py XLK taxable
XLK buy and hold 486% vs 680% for trend following since 12/31/98
Trend following outperformed through 12/30/22
```

trendFollowing.py will create a CSV output file showing the post-tax monthly return for both strategies by month (e.g. SPY-return-taxable.csv)

### Download additional monthly data from AlphaVantage.co

Create a file .apikey.txt with your own key from [AlphaVantage.co](https://www.alphavantage.co/support/#api-key)

Download monthly data for another ETF or stock

```
# python3 getData.py BRK-A
Output saved to BRK-A-monthly.csv

# python3 trendFollowing.py BRK-A
BRK-A buy and hold 844% vs 562% for trend following since 12/31/99
Trend following outperformed through 02/27/09
```

For simplicity, getData.py will report a warning if the adjusted close price is 2x or 1/2 the historical closing price. 
AlphaVantage's API doesn't include a stock split column and the adjusted close column reflects both dividend adjustments and stock splits.

However, it is possible to manually adjust for the split in the CSV file (as has been done for QQQ). For future imports, getData.py will only add new rows for newer months.

```
# python3 getData.py QQQ
A stock split may have occurred on 02/29/00 because adjusted close 91.8957 != historic 213.5000
This is only intended to backtest ETFs which do not have stock splits
A stock split may have occurred on 01/31/00 because adjusted close 77.2182 != historic 179.4000
This is only intended to backtest ETFs which do not have stock splits
A stock split may have occurred on 12/31/99 because adjusted close 78.6817 != historic 182.8000
This is only intended to backtest ETFs which do not have stock splits
Output saved to QQQ-monthly.csv
```
