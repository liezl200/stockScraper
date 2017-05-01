import urllib
import os

# the CSV download link with start date and end date constant
CSV_LINK = 'http://www.google.com/finance/historical?q=<SYMBOL>&startdate=May+3%2C+2012&enddate=Apr+30%2C+2017&num=30&output=csv'

# where all the CSV files will go
STOCK_DIR = './rawCSV/'

# global stock symbol list that should be read in from ./stocklist.txt
stockSymbols = []

def makeDir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

def getCSV(symbol):
	url = CSV_LINK.replace('<SYMBOL>', symbol)
	urllib.urlretrieve (url, STOCK_DIR + symbol + '.csv')

makeDir(STOCK_DIR) # required before calling getCSV()
getCSV('GOOG')