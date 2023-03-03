from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pymysql
import numpy as np
import pandas as pd
import time
import random

# 資料庫設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "crypto",
    "charset": "utf8"
}


# 建立Connection物件
conn = pymysql.connect(**db_settings)
# 建立Cursor物件
cursor = conn.cursor()
#如果已經存在的話就刪除
cursor.execute('DROP TABLE IF EXISTS data_ptt')
#建立table
sql = '''CREATE TABLE data_ptt(
            title VARCHAR(255),
            url VARCHAR(255));'''
cursor.execute(sql)
conn.commit()

#PTT DigiCurrency
url = "https://www.ptt.cc/bbs/DigiCurrency/index.html"
for i in range(2):#爬取兩頁
    g = requests.get(url)
    soup = BeautifulSoup(g.text,"html.parser")#將網頁資料以html.parser
    title = soup.select("div.title a") #標題
    u = soup.select("div.btn-group.btn-group-paging a") #a標籤
    url = "https://www.ptt.cc"+ u[1]["href"] #上一頁的網址
    
    for titles in title: #印出網址跟標題
         cursor.execute("INSERT INTO data_ptt(title, url) VALUES ('%s', '%s');" %(titles.text, titles["href"]) )
         conn.commit()

#取出全部資料
cursor.execute("SELECT * FROM data_ptt")
data_ptt = cursor.fetchall()    
data_str = '\n'.join(str(v) for v in data_ptt)#轉Str.  
print(data_str)