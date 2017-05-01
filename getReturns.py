import urllib
import os
import csv

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

def makeDir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

def getCSVFilename(symbol):
  return STOCK_DIR + symbol + '.csv'

def getCSV(symbol):
  url = CSV_LINK.replace('<SYMBOL>', symbol)
  urllib.urlretrieve (url, getCSVFilename(symbol))

def readListFromFile(fname):
  with open(fname) as f:
    lines = f.readlines()
    lineList = [x.strip() for x in lines]
    return lineList

def getAllStockCSVs():
  print 'Scraping', len(stockSymbols), 'stocks...'
  makeDir(STOCK_DIR) # required before calling getCSV()
  for symbol in stockSymbols:
    getCSV(symbol)
  print 'Finished scraping', len(stockSymbols), 'stocks'

def readAllStockPrices():
  print 'Reading closing prices into memory'
  CLOSE_COLUMN_INDEX = 4
  for symbol in stockSymbols:
    with open(getCSVFilename(symbol), 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      closePriceList = []
      for row in reader:
        closePriceList.append(row[CLOSE_COLUMN_INDEX])
      closePrices[symbol] = closePriceList[1:] # ignore the 'Close' header by slicing
  print 'Done reading closing prices into memory'

stockSymbols = readListFromFile(STOCK_LIST_FILENAME)
# getAllStockCSVs() # comment out this line if you already have all 505 CSV files in rawCSV
readAllStockPrices()
