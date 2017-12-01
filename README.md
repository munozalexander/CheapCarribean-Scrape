# CheapCarribean-Scrape

This repo scrapes and crawls [CheapCarribean.com](https://www.cheapcaribbean.com) to find cheapest vacations. Results that satisfy the constraints (within date range, number of nights stayed longer than minimum night requirement, and price below maximum price) are printed to the console.

Run this repo with default parameters with `python crawler.py`

Run this repo with customized parameters by replacing parameters in the following block:
```python
from crawler import Crawler
crawler = Crawler(earliestDeparture = '3/10/2018', \
                  latestArrival = '3/18/2018', \
                  minNights = 4, \
                  maxPrice = 850, \
                  includeMexico = False)
crawler.crawl()
```
The parameters are:
* earliestDeparture : string for earliest possible departure date, "MM/DD/YYYY"
* latestArrival : string for latest possible arrival date, "MM/DD/YYYY"
* minNights : int for minimum nights to stay
* maxPrice : int for maximum price willing to pay
* includeMexico : bool for crawling locations in Mexico
