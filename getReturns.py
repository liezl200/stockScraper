import urllib
import os
import csv
import math

# the CSV download link with start date and end date constant
CSV_LINK = 'http://www.google.com/finance/historical?q=<SYMBOL>&startdate=Apr+3%2C+2012&enddate=Apr+30%2C+2017&num=30&output=csv'

# where all the CSV files will go
STOCK_DIR = './rawCSV/'

# should be a file that has one stock symbol per line
STOCK_LIST_FILENAME = './stocklist.txt'

# file for the output csv
FIVE_YEAR_LOG_RETURNS_FNAME = './five_year_500.csv'

# file for the output csv
FIVE_YEAR_PRICES_FNAME = './five_year_500_prices.csv'

# global stock symbol list that should be read in from ./stocklist.txt
stockSymbols = []

# global list of dates
dateLabels = []

# global close prices list for every stock symbol {symbol: [close1, close2, ...]}
closePrices = {}

# global log returns list (log(close_recent) - log(close_past))
logReturns = {}

# makes a new directory if it doesn't exist
def makeDir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

# helper function to get filename for a particular symbol
def getCSVFilename(symbol):
  return STOCK_DIR + symbol + '.csv'

# download the CSV file from Google Finance
def getCSV(symbol):
  url = CSV_LINK.replace('<SYMBOL>', symbol)
  urllib.urlretrieve (url, getCSVFilename(symbol))

def getCSVWithNYSE(symbol):
  url = CSV_LINK.replace('<SYMBOL>', 'NYSE%3A' + symbol)
  urllib.urlretrieve (url, getCSVFilename(symbol))

# read every line into a list of lines from fname, then return the list
def readListFromFile(fname):
  with open(fname) as f:
    lines = f.readlines()
    lineList = [x.strip() for x in lines]
    return lineList

# download the CSV files for every stock from Google Finance
def getAllStockCSVs():
  print 'Scraping', len(stockSymbols), 'stocks...'
  makeDir(STOCK_DIR) # required before calling getCSV()
  for symbol in stockSymbols:
    if symbol != 'NWL': # skip NWL, for some reason auto download doesn't work for it
      getCSV(symbol)
    else:
      getCSVWithNYSE('NWL')
  print 'Finished scraping', len(stockSymbols), 'stocks'

# read the closing prices for every stock into memory (stored in closePrices global dict)
# requires that stockSymbols is populated
def readAllStockPrices():
  print 'Reading closing prices into memory'
  CLOSE_COLUMN_INDEX = 4
  for symbol in stockSymbols:
    with open(getCSVFilename(symbol), 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      closePriceList = []
      skipFirst = True
      for row in reader:
        if skipFirst:
          skipFirst = False
        else:
          closePriceList.append(float(row[CLOSE_COLUMN_INDEX]))
    closePrices[symbol] = closePriceList
  print 'Done reading closing prices into memory'

# reads and returns the date column from one stock CSV
# requires that stockSymbols is populated and that we have all stock CSVs downloaded
def readDateColumn():
  DATE_COLUMN_INDEX = 0
  with open(getCSVFilename('GOOG'), 'rb') as csvfile: # doesn't matter which stock, just read the date column
    dates = []
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      dates.append(row[DATE_COLUMN_INDEX])
    return dates[1:]

# helper function that takes an array of prices and returns the log returns
def calculateLogReturns(prices): # TODO: calculate first row?
  returns = []
  for i in range(len(prices)-1):
    returns.append(math.log(prices[i]) - math.log(prices[i+1]))
  return returns

# calculates log returns for every stock and stores it in memory (stored in the logReturns global dict)
# requires that stockSymbols and closePrices are populated
def calculateAllLogReturns():
  print 'Calculating log returns for', len(stockSymbols), 'stocks...'
  for symbol in stockSymbols:
    logReturns[symbol] = calculateLogReturns(closePrices[symbol])
  print 'Done calculating log returns for', len(stockSymbols), 'stocks'

# requires dates, stockSymbols, logReturns
# writes to a file w/ each row corresponding to one timestamp
def writeAllLogReturns(onlyFullHistories=True):
  print 'Writing log returns for', len(stockSymbols), 'stocks...'
  outFile = open(FIVE_YEAR_LOG_RETURNS_FNAME, 'w')
  # write header row
  outFile.write('Date')
  for symbol in stockSymbols:
    outFile.write(',' + symbol)
  outFile.write('\n')

  fullStockSymbols = stockSymbols[:]
  removedStockSymbols = []
  if onlyFullHistories:
    # check if the symbol has a full history. make onlyFullHistories=True if you want all stock symbols to be written even if they don't have a full history
    maxTimestamps = len(logReturns['GOOG'])
    for symbol in stockSymbols:
      if len(logReturns[symbol]) < maxTimestamps:
        fullStockSymbols.remove(symbol)
        removedStockSymbols.append((symbol, len(logReturns[symbol])))

  # write data rows
  dates = dateLabels[1:] # TODO: once we figure out how to calculate first row, add most recent date back in
  for i in range(len(dates)):
    outFile.write(dates[i]) # write the date

    # for every date, we loop through every stock and get the entry for that date to add to the row
    for symbol in fullStockSymbols:
      if len(logReturns[symbol]) > i:
        # note ZTS ends at Feb 1, 2013 -- if a stock doesn't have a full 5 year history then we'll leave the unfilled timestamps blank
        outFile.write(',' + str(logReturns[symbol][i]))
      else:
        outFile.write(',')
    outFile.write('\n')
  outFile.close()
  print 'Done writing log returns for', len(fullStockSymbols), 'stocks.',
  if onlyFullHistories:
    print len(stockSymbols) - len(fullStockSymbols), 'had an incomplete history for the specified date range.'
    print 'Removed symbols: ', removedStockSymbols

def writeAllPrices(onlyFullHistories=True):
  print 'Writing prices for', len(stockSymbols), 'stocks...'
  outFile = open(FIVE_YEAR_PRICES_FNAME, 'w')
  # write header row
  outFile.write('Date')
  for symbol in stockSymbols:
    outFile.write(',' + symbol)
  outFile.write('\n')

  fullStockSymbols = stockSymbols[:]
  removedStockSymbols = []
  if onlyFullHistories:
    # check if the symbol has a full history. make onlyFullHistories=True if you want all stock symbols to be written even if they don't have a full history
    maxTimestamps = len(closePrices['GOOG'])
    for symbol in stockSymbols:
      if len(closePrices[symbol]) < maxTimestamps:
        fullStockSymbols.remove(symbol)
        removedStockSymbols.append((symbol, len(closePrices[symbol])))

  # write data rows
  dates = dateLabels[1:]
  for i in range(len(dates)):
    outFile.write(dates[i]) # write the date

    # for every date, we loop through every stock and get the entry for that date to add to the row
    for symbol in fullStockSymbols:
      if len(closePrices[symbol]) > i:
        # note ZTS ends at Feb 1, 2013 -- if a stock doesn't have a full 5 year history then we'll leave the unfilled timestamps blank
        outFile.write(',' + str(closePrices[symbol][i]))
      else:
        outFile.write(',')
    outFile.write('\n')
  outFile.close()
  print 'Done writing prices for', len(fullStockSymbols), 'stocks.',
  if onlyFullHistories:
    print len(stockSymbols) - len(fullStockSymbols), 'had an incomplete history for the specified date range.'
    print 'Removed symbols: ', removedStockSymbols


stockSymbols = readListFromFile(STOCK_LIST_FILENAME)
# getAllStockCSVs() # comment out this line if you already have all 505 CSV files in rawCSV
dateLabels = readDateColumn()

readAllStockPrices() # read all closing prices of every stock into memory
calculateAllLogReturns() # calculate log returns for every stock
writeAllLogReturns()

writeAllPrices()
