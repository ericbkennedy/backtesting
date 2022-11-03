#
# Download monthly ETF prices from https://www.alphavantage.co/ for
# backtesting trendFollowing.py
#
# Copyright 2022 Eric Kennedy

import csv
import requests
import sys

MISSING_KEY_MSG = 'Create a file .apikey.txt with your own key from https://www.alphavantage.co/support/#api-key'
apiKeyFilename = '.apikey.txt'
apiKey = 'demo'
ticker = ''

try:
    with open(apiKeyFilename, 'r') as keyFile:
        apiKey = keyFile.readline()
except Exception as e:
    print(MISSING_KEY_MSG)
    exit()

if len(sys.argv) < 2:
    print('Enter ticker e.g.: python3 getData.py SPY')
    exit()
else:
    ticker = sys.argv[1]

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={ticker}&outputsize=full&datatype=csv&apikey={apiKey}'

r = requests.get(url)

output = [] # list to hold columns after removing high, low and volume

csvInput = r.text.splitlines()
print(csvInput)

for line in csvInput:
    row = line.split(',')
    if len(row) == 1: # allow trailing empty line
        continue
    elif len(row) != 8:
        print(f'Unexpected row length {len(row)} in {row}')
        exit()
    closingDate = row[0]
    openPrice = row[1]
    # skip high in row[2]
    # skip low in row[3]
    closePrice = row[4]
    adjClose = row[5]
    # skip volume in row[6]
    divAmount = row[7]
    output.append((closingDate, openPrice, closePrice, adjClose, divAmount))

outputFilename = f'{ticker}-monthly.csv'

with open(outputFilename, mode='w', newline='') as csvOutput:
    csvWriter = csv.writer(csvOutput, delimiter=',', quotechar="'")
    for row in output:
        csvWriter.writerow(row)

print(f'Output saved to {outputFilename}')
