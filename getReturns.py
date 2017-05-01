import urllib
import os
import csv
import math

# the CSV download link with start date and end date constant
CSV_LINK = 'http://www.google.com/finance/historical?q=<SYMBOL>&startdate=May+3%2C+2012&enddate=Apr+30%2C+2017&num=30&output=csv'

# where all the CSV files will go
STOCK_DIR = './rawCSV/'

# should be a file that has one stock symbol per line
STOCK_LIST_FILENAME = './stocklist.txt'

# global stock symbol list that should be read in from ./stocklist.txt
stockSymbols = []

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
    getCSV(symbol)
  print 'Finished scraping', len(stockSymbols), 'stocks'

# read the closing prices for every stock into memory (stored in closePrices global dict)
def readAllStockPrices():
  print 'Reading closing prices into memory'
  CLOSE_COLUMN_INDEX = 4
  for symbol in stockSymbols:
    with open(getCSVFilename(symbol), 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      closePriceList = []
      for row in reader:
        closePriceList.append(float(row[CLOSE_COLUMN_INDEX]))
      closePrices[symbol] = closePriceList[1:] # ignore the 'Close' header by slicing
  print 'Done reading closing prices into memory'

# reads and returns the date column from one stock CSV
def readDateColumn():
  DATE_COLUMN_INDEX = 0
  with open(getCSVFilename('GOOG'), 'rb') as csvfile: # doesn't matter which stock, just read the date column
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      dates.append(row[DATE_COLUMN_INDEX])
  return dates

# takes an array of prices and returns the log returns
def calculateLogReturns(prices):
  returns = []
  for i in range(t-1):
    returns.append(math.log(prices[i+1]) - math.log(prices[i]))
  return returns

# calculates log returns for every stock and stores it in memory (stored in the logReturns global dict)
def calculateAllLogReturns():
  print 'Calculating returns for', len(stockSymbols), 'stocks...'
  for symbol in stockSymbols:
    logReturns[symbol] = calculateLogReturns(symbol)
  print 'Calculating returns for', len(stockSymbols), 'stocks'

stockSymbols = readListFromFile(STOCK_LIST_FILENAME)
# getAllStockCSVs() # comment out this line if you already have all 505 CSV files in rawCSV
dates = readDateColumn()
readAllStockPrices() # read all closing prices of every stock into memory
calculateAllLogReturns() # calculate log returns for every stock


