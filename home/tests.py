# for i in range (1 ,11):
#     print(i)

# x = input(("x :" ))
# y = input(("y :" ))
# print(int(x) * int(y))

# 1 人民幣 等於
# 1.14 港幣

# x = input("人民幣: ")
# y = round(int(x) * 1.14, 2)
# print("港幣:", y)

# for i in range(1,6,1):
#      print("*"*i)


# for i in range(5,0,-1):
#     print(" " * (6-i) + "*" * (2*i-1))

import matplotlib.pyplot as plt
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pymysql
import pandas as pd
import plotly.express as px
from IPython.display import HTML

# 資料庫設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "crypto",
    "charset": "utf8",
}

# 建立Cursor物件
conn = pymysql.connect(**db_settings)
cursor = conn.cursor()

 #如果crypto已經存在的話就刪除
cursor.execute('DROP TABLE IF EXISTS data_ptt')

try:
    conn.ping(reconnect=True)#檢查連結是否斷開，如是重連
    #建立table
    sql = '''CREATE TABLE data_ptt(
                title VARCHAR(255),
                url VARCHAR(255));'''
    cursor.execute(sql)
    conn.commit()

    #PTT DigiCurrency
    url = "https://www.ptt.cc/bbs/DigiCurrency/index.html"
    for i in range(2):#爬取兩頁
        g = requests.get(url,timeout=None)
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
    print(type(data_ptt))    
    data_ptt_str = '\n'.join(str(v) for v in data_ptt)#元組tuple轉字串Str
except Exception as ex:#例外錯誤處理
    conn.rollback()
    print(ex)

def Ptt(request):
    return render(request, 'crypto.html',{
                'data_ptt' : data_ptt_str
    })
