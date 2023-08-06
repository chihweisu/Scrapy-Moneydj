import scrapy
import logging


class EtfSpider(scrapy.Spider):
    name = "etf"
    allowed_domains = ["www.moneydj.com"]
    # start_urls = ["https://www.moneydj.com/etf/x/default.xdjhtm"]

    def start_requests(self):
        # etf_codes = ['00713.TW'] 
        etf_codes = ['00713.TW','00878.TW','0056.TW','0050.TW','006208.TW','00679B.TW','00687B.TW','00719B.TW']  # 要獲取的ETF代碼列表
        pages=['0002', '0005', '0007']  #技術分析/配息紀錄/持股狀況

        for etf_code in etf_codes:
            for page in pages:
                url = 'https://www.moneydj.com/ETF/X/Basic/Basic{}.xdjhtm?etfid={}'.format(page, etf_code)
                if page == '0002':
                    yield scrapy.Request(url, callback=self.parse_history, meta={'etf_code': etf_code})
                if page == '0005':
                    yield scrapy.Request(url, callback=self.parse_dividend, meta={'etf_code': etf_code})
                elif page == '0007':
                    yield scrapy.Request(url, callback=self.parse_holdings, meta={'etf_code': etf_code})
    
    def parse_dividend(self, response):
        etf_code = response.request.meta['etf_code']
        table=response.xpath("//table[@class='datalist']")
        rows = table.xpath('.//tr')

        for row in rows[1:5]:  # 跳過表頭行，從第二行開始讀取資料
            # 解析每一行的資料
            yield{
                'etf_code': etf_code,
                'ex_date' : row.xpath(".//td[2]/text()").get(),
                'pay_date' : row.xpath(".//td[3]/text()").get(),
                'currency' : row.xpath(".//td[4]/text()").get(),
                'amount' : row.xpath(".//td[7]/text()").get(),
            }

    def parse_holdings(self, response):
        etf_code = response.request.meta['etf_code']
        table=response.xpath("//table[@class='datalist']")[-1] #資料型態:list
        rows = table.xpath('.//tr')

        for row in rows[1:6]:  # 跳過表頭行，從第二行開始讀取資料
            if 'B' in etf_code :
                yield{
                    'etf_code' : etf_code,
                    'holding' : row.xpath(".//td[1]/text()").get(),
                    'ratio' : row.xpath(".//td[2]/text()").get()+'%',
                }
            else:
                yield{
                    'etf_code' : etf_code,
                    'holding' : row.xpath(".//td[1]//a/text()").get(),
                    'ratio' : row.xpath(".//td[2]/text()").get()+'%',
                }


    def parse_history(self, response):
        etf_code = response.request.meta['etf_code']
        table=response.xpath("//table[@class='DataTable']")[1] #資料型態:list 第一個表格
        row = table.xpath('.//tr[1]')  #第一行
        yield{
                'etf_code' : etf_code,
                'price' : row.xpath(".//td[2]/text()").get() #第二格
            }


