# stockScraper
scrape google finance

## Input / Output

1. Input: `stocklist.txt` is a list of symbols to scrape the data for. Format:

```
MMM
ABT
ABBV
ACN
ATVI
AYI
...
```

1. Output: `five_year_500.csv` a matrix of log returns (every row is one date and every column is one stock symbol). Note: if the date range goes before the first historical price, then the log returns before the first historical price are left blank.

## How to run
`python getReturns.py`