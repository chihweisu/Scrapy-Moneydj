# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SQLlitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect('etf_info.db')
        self.c = self.connection.cursor()

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS etf_status(
                etf_code TEXT NOT NULL UNIQUE PRIMARY KEY,
                price REAL NOT NULL
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS etf_holdings(
                holding_id	INTEGER PRIMARY KEY,
                etf_code	TEXT NOT NULL,
                holding	TEXT NOT NULL,
                ratio	TEXT NOT NULL
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS etf_dividends(
                dividends_id	INTEGER PRIMARY KEY,
                etf_code	TEXT NOT NULL,
                ex_date	TEXT NOT NULL,
                pay_date	TEXT NOT NULL,
                amount	REAL NOT NULL,
                currency	TEXT NOT NULL
            )
        ''')

        # 刪除 etf_holdings 表格的資料
        self.c.execute('''DELETE FROM etf_holdings''')

        # 刪除 etf_dividends 表格的資料
        self.c.execute('''DELETE FROM etf_dividends''')

        self.connection.commit()


    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if 'price' in item:
            self.c.execute('''INSERT OR REPLACE INTO etf_status (etf_code, price) VALUES(?,?)''',  
            (
                item.get('etf_code'),
                float(item.get('price')),
            ))
        elif 'holding' in item:
            self.c.execute('''INSERT OR REPLACE INTO etf_holdings (etf_code, holding, ratio) VALUES(?,?,?)''',  
            (
                item.get('etf_code'),
                item.get('holding'),
                item.get('ratio'),
            ))
        elif 'ex_date' in item:
            self.c.execute('''INSERT OR REPLACE INTO etf_dividends (etf_code, ex_date, pay_date, amount, currency) VALUES(?,?,?,?,?)''',  
            (
                item.get('etf_code'),
                item.get('ex_date').replace('/', '-'),
                item.get('pay_date').replace('/', '-'),
                float(item.get('amount')),
                item.get('currency'),
            ))
        self.connection.commit()
        return item
