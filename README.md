# ETF Data Scraper and Emailer


## Introduction
This is a Scrapy project designed to scrape ETF data and store it in a SQLite3 database. 
The scraper extracts essential information from various ETF sources and saves it for further analysis. 
Additionally, the project includes a functionality to generate an HTML table from the stored data and send it to your email.


## Installation and Usage

相關模組
```
scrapy==2.8.0
pandas==2.0.3
python-decouple==3.8
pretty-html-table==0.9.16
```

執行`starter.py`即可自動完成爬蟲、建立資料庫、後處理和寄信等動作
```python
python starter.py
```

## Features
* **Scrapy-based** web scraper to collect ETF data from multiple sources.
* **SQLite3 database** for efficient storage and retrieval of scraped data.
* Support for generating an HTML table and **sending it via email**.

