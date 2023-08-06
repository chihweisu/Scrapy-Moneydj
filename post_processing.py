import sqlite3
from datetime import datetime

def get_latest_info(etf_code):
    c.execute('''
    SELECT *
    FROM etf_dividends
    WHERE ex_date <= ? AND etf_code = ?
    ORDER BY ex_date DESC
    LIMIT 1
    ''', (datetime.now().strftime('%Y-%m-%d'), etf_code)
    )
    return c.fetchone()

def get_biggest_holding(etf_code):
    c.execute('''
    SELECT *
    FROM etf_holdings
    WHERE etf_code = ?
    ORDER BY ratio DESC
    LIMIT 1
    ''', (etf_code,)
    )
    return c.fetchone()  

def add_column_to_etf_status(c):
    try:
        # 使用 ALTER TABLE 添加新的欄位
        c.execute('''ALTER TABLE etf_status ADD COLUMN latest_pay_date TEXT''')
        c.execute('''ALTER TABLE etf_status ADD COLUMN latest_pay_amount TEXT''')
        c.execute('''ALTER TABLE etf_status ADD COLUMN latest_currency TEXT''')
        c.execute('''ALTER TABLE etf_status ADD COLUMN latest_yield TEXT''')
        c.execute('''ALTER TABLE etf_status ADD COLUMN biggest_holding TEXT''')
        c.execute('''ALTER TABLE etf_status ADD COLUMN holding_ratio TEXT''')
    except sqlite3.OperationalError as e:
        print("重複欄位:", e)
        pass
    
    #填入新欄位的資料
    c.execute('''SELECT * FROM etf_status''')
    status_data=c.fetchall()
    for i in range(len(status_data)):
        etf_code= status_data[i][0]
        price = status_data[i][1]
        result = get_latest_info(etf_code)
        result2 = get_biggest_holding(etf_code)
        if result:
            latest_pay_date, latest_pay_amount, latest_currency = result[3:]
            latest_yield = round(latest_pay_amount/price*100,2)
            c.execute('''
                UPDATE etf_status
                SET latest_pay_date = ?,
                    latest_pay_amount = ?,
                    latest_currency = ?,
                    latest_yield = ?
                WHERE etf_code = ?
            ''', (latest_pay_date, latest_pay_amount, latest_currency, str(latest_yield)+'%', etf_code))

        if result2:
            biggest_holding, holding_ratio = result2[2:]
            c.execute('''
                UPDATE etf_status
                SET biggest_holding = ?,
                    holding_ratio = ?
                WHERE etf_code = ?
            ''', (biggest_holding, holding_ratio, etf_code))





if __name__ == "__main__":
    # 建立資料庫連接
    conn = sqlite3.connect("etf_info.db")
    c = conn.cursor()

    add_column_to_etf_status(c)

    # 提交變更
    conn.commit()

    # 關閉連接
    conn.close()