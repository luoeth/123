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
cursor.execute('DROP TABLE IF EXISTS data_defi_chainsTVL')
# try:
conn.ping(reconnect=True)#檢查連結是否斷開，如是重連
    #建立table
sql = '''CREATE TABLE data_defi_chainsTVL(
                name text,
                tvl text);'''
cursor.execute(sql)
conn.commit()

# DefiLlama / chains
r = requests.get('https://api.llama.fi/v2/chains',timeout=None)
json = r.json()
for j in json:
        try:
                cursor.execute("INSERT INTO data_defi_chainsTVL(name, tvl) VALUES ('%s', '%s');" %(j["name"], j["tvl"]))
                conn.commit()
        except Exception as ex:#例外錯誤處理 
                print(ex)

try:
    cursor.execute("SELECT * FROM data_defi_chainsTVL")
    data_tvl = cursor.fetchall()
    tvl = list(data_tvl)#轉list
except Exception as ex:#例外錯誤處理 
    print(ex)

df = pd.DataFrame(tvl,
    columns=['chains', 'tvl'])

fig = px.pie(df, values='tvl', names='chains', title='TVL of all Chains')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()
