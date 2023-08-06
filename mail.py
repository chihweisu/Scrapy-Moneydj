import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pretty_html_table import build_table
import pandas as pd
import os
from decouple import config



def get_etf_status_data():

    # 取得當前的工作目錄
    current_directory = os.getcwd()
    # # 印出當前路徑
    # print("當前路徑：", current_directory)

    # 確認 etf_info.db 資料庫的路徑
    db_path = os.path.join(current_directory, "moneydj", "etf_info.db")

    # 建立資料庫連接
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 取得 etf_status 資料
    c.execute('''SELECT * FROM etf_status''')
    data = c.fetchall()
    
    # 取得欄位名稱
    column_names = [description[0] for description in c.description]

    df = pd.DataFrame(data, columns=column_names )

    # 關閉連接
    conn.close()

    return df

def send_email(sender, password, receiver, subject, content, attachment_path=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # 拼接郵件內容

    # 加入郵件內文
    msg.attach(MIMEText(content, "html"))
    msg_body = msg.as_string() 


    # 加入附件
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            attachment = MIMEApplication(f.read(), Name=attachment_path.split('/')[-1])
        attachment['Content-Disposition'] = 'attachment; filename="%s"' % attachment_path.split('/')[-1]
        msg.attach(attachment)

    # 建立 SMTP 連線
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # 登入帳號
    server.login(sender, password)

    # 寄送郵件
    server.sendmail(sender, receiver,  msg_body)

    # 關閉連線
    server.quit()

if __name__ == "__main__":
    # 取得 etf_status 資料
    etf_status_df = get_etf_status_data()
    content = build_table(etf_status_df , "orange_dark")

    # 設定郵件相關資訊
    subject = "ETF Status Report"
    receiver= config('MAIL_RECEIVER')  # 收件者的電子郵件地址
    smtp_server = "outlook.office365.com"
    smtp_port = 587
    sender = config('EMAIL_USERNAME')
    password = config('EMAIL_PASSWORD')

    # 寄送郵件並附上附件
    send_email(sender, password, receiver, subject, content)

    print("郵件寄送成功！")