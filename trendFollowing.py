#
# Calculate the difference in return for buy-and-hold vs trend following
# where closes below an ETF's 10 month simple moving average will sell and go to cash.
#
# This trend following approach outperformed the S&P 500 ETF SPY from 1998 through
# the 2001 and 2008 recessions. However it has lagged buy-and-hold after 2019,
# especially after the tax consequences of selling are taken into account.
#
# The only major sector ETF where trend following is still outperforming is the
# XLK Technology ETF. It has the largest S&P 500 sector weight so it could
# make sense to use trend following for that portion of an equity portfolio.
#
# Copyright 2022 Eric Kennedy

import sys
import csv

DIVIDEND_TAX_RATE = 0.15
CAPITAL_GAIN_RATE = 0.20
INITAL_BALANCE = 10000.0
isTaxableAccount = False

if len(sys.argv) < 2:
    raise Exception('Enter ticker (and optionally taxable)')
else:
    ticker = sys.argv[1]
    if len(sys.argv) == 3 and 'taxable' == sys.argv[2]:
        isTaxableAccount = True

months, output = [], []

with open(f'{ticker}-monthly.csv', newline='') as csvInput:
    reader = csv.reader(csvInput, delimiter=',', quotechar='|')
    for row in reader:
        if len(row) == 5:
            closingDate = row[0]
            if closingDate != 'timestamp': # skip header
                openPrice = float(row[1]) # don't call it open to avoid redefining open()
                closePrice = float(row[2])
                # adjClose = float(row[3]) # unused since it double counts dividend adjustments
                dividend = float(row[4])
                monthlyData = (closingDate, openPrice, closePrice, dividend)
                months.insert(0, monthlyData) # insert older months at start for ascending order
        else:
            print('Check CSV format', *row)
            raise ValueError('Invalid row length', len(row))

last10closes = []
rollingSum = movingAverage = shares = bhShares = 0.0
initialMonth = months[0][0]
cash = costBasis = INITAL_BALANCE

# SPY was above the 10 month MA at the end of October 1998 (110 close v 106.66 MA) so start both long
initialPrice = months[0][1]
trendFollowingOutperformingDate = months[0][0] # Used for 'Trend following outperformed through {date}'
shares = round(cash / initialPrice, 2)
cash = 0.0 # since we start out long
bhShares = shares

for index, (closingDate, openPrice, closePrice, dividend) in enumerate(months):
    last10closes.append( (closingDate, openPrice, closePrice, dividend) )
    rollingSum += closePrice
    taxes = 0
    comments = ''

    if index + 1 < len(months):
        nextOpen = months[index + 1][1]
    else:
        nextOpen = closePrice # to calculate buying or selling for the final month

    if dividend > 0.0: # reinvest dividend if long
        if isTaxableAccount:
            dividend *= (1 - DIVIDEND_TAX_RATE) # reduce by tax rate

        bhShares += round(bhShares * dividend / closePrice, 2)

        if shares > 0.0: # will only get the dividend if long but could still sell based on MA
            cash += round(shares * dividend, 2)

    if len(last10closes) > 10: # drop entry from 11 months ago
        droppedMonth = last10closes.pop(0)
        rollingSum -= droppedMonth[1] # closing price is index = 1

    if len(last10closes) == 10:
        movingAverage = round(rollingSum/10, 2)
        if closePrice >= movingAverage:
            if shares == 0.0:
                shares = round(cash / nextOpen, 2)
                comments = f'Bought {shares} at {nextOpen}'
                cash = 0.0
        else: # close below MA so sell if long or stay in cash
            if shares > 0.0:
                cash += round(shares * nextOpen, 2)
                comments = f'Sold {round(shares, 2)} at {nextOpen}'
                if isTaxableAccount and cash > costBasis:
                    taxes = round((cash - costBasis) * CAPITAL_GAIN_RATE, 2) # deduct taxes
                    comments += f' and paid {round(taxes)} on gain {round(cash - costBasis)}'
                    cash -= taxes
                    costBasis = cash
                shares = 0

    if len(last10closes) < 10 or shares > 0.0: # reinvest dividend until 10 month MA can be calculated
        shares += round(shares * dividend / closePrice, 2)
        cash = 0.0

    bhValue = round(closePrice * bhShares)
    tfValue = round(cash + closePrice * shares)
    if tfValue > bhValue:
        trendFollowingOutperformingDate = closingDate

    output.append((closingDate,
                   openPrice,
                   closePrice,
                   movingAverage,
                   bhShares,
                   '${:,}'.format(bhValue),
                   shares,
                   '${:,}'.format(tfValue),
                   taxes,
                   comments))

buyHoldReturn = round(100 * (closePrice * bhShares) / INITAL_BALANCE)
trendFollowingReturn = round(100 * (closePrice * shares + cash) / INITAL_BALANCE)

print(f'{ticker} buy and hold {buyHoldReturn}% vs {trendFollowingReturn}% for trend following since {initialMonth}')

if trendFollowingOutperformingDate == initialMonth:
    print('Trend following never outperformed buy-and-hold')
else:
    print(f'Trend following outperformed through {trendFollowingOutperformingDate}')

filename = ticker + '-return'
if isTaxableAccount:
    filename += '-taxable'

with open(f'{filename}.csv', mode='w', newline='') as csvOutput:
    csvWriter = csv.writer(csvOutput, delimiter=',', quotechar='"')
    csvWriter.writerow(['Month end',
                        'Open at start of month',
                        'Close at end of month',
                        '10 month moving average',
                        'Buy and hold shares',
                        'Buy and hold value',
                        'Trend following shares',
                        'Trend following value',
                        'Taxes paid',
                        'Comments']);
    for row in output:
        csvWriter.writerow(row)