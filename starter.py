import subprocess
import os


# 設定 Scrapy 專案的路徑
project_path = os.path.dirname(os.path.abspath(__file__))  #D:\Python_Project\MyScrapy\moneydj
print("專案路徑：", project_path)

 #取得當前的工作目錄
current_directory = os.getcwd() #D:\Python_Project\MyScrapy
print("當前路徑：", current_directory)

# 呼叫 Scrapy 的執行命令
scrapy_result = subprocess.run(['scrapy', 'crawl', 'etf'], cwd=project_path)

# 檢查 Scrapy 爬蟲是否正常完成
if scrapy_result.returncode == 0:
    print("Scrapy 爬蟲執行成功！")
    # 呼叫 post_processing.py
    post_processing_result  = subprocess.run(['.venv\Scripts\python', 'post_processing.py'], cwd=project_path)

    # 檢查 post_processing.py 是否正常完成
    if post_processing_result.returncode == 0:
        # 檢查 post_processing.py 是否正常完成
        print("post_processing.py 執行成功！")
        # 呼叫 mail.py
        mail_result = subprocess.run(['.venv\Scripts\python', 'moneydj/mail.py'])
        
        # 檢查 mail.py 是否正常完成
        if mail_result.returncode == 0:
            print("mail.py 執行成功！")
        else:
            print("mail.py 執行失敗！")
    else:
        print("post_processing.py 執行失敗！")
else:
    print("Scrapy 爬蟲執行失敗！")

