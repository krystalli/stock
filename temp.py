# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date
import numpy as np
import pandas  as pd
import csv
import unicodecsv
import pickle

def getTSEStcokInfo():
    r = requests.post("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    soup = BeautifulSoup(r.text, "lxml")
    data = {'股票代號':[], '股票名稱':[]}
    stopScan = False;
    for idx, tr in enumerate(soup.select('table')[1].find_all('tr')):
        if idx > 1:
            try:
                tds = tr.find_all('td')
                stock = tds[0].contents[0].split('\u3000',1)
                if "1312A" in stock[0]:
                    stopScan = False;
                if stopScan == False:
                    str0 = stock[0].strip()
                    if str0.startswith('00'):
                        str0 = str0.replace("00", "I", 1)
                    data['股票代號'].append(str0)
                    data['股票名稱'].append(stock[1].strip())
                    #print(data)
                if "9958" in stock[0]:
                    stopScan = True;
            except TypeError:
                print ("Oops!  That was no valid number.  Try again...")
    # 把 data 放到 DataFrame 裡面
    df = pd.DataFrame(data)
    return df

def getOTCStcokInfo():
    r = requests.post("https://isin.twse.com.tw/isin/C_public.jsp?strMode=4")
    soup = BeautifulSoup(r.text, "lxml")
    data = {'股票代號':[], '股票名稱':[]}
    startAdd = False;
    for idx, tr in enumerate(soup.select('table')[1].find_all('tr')):
        if idx > 7:
            try:
                tds = tr.find_all('td')
                stock = tds[0].contents[0].split('\u3000',1)
                if "006201" in stock[0]:
                    startAdd = True;
                if startAdd == True:
                    str0 = stock[0].strip()
                    if str0.startswith('00'):
                        str0 = str0.replace("00", "I", 1)
                    data['股票代號'].append(str0)
                    data['股票名稱'].append(stock[1].strip())
                    print(data)
                if "911613" in stock[0]:
                    startAdd = False;
            except TypeError:
                print ("Oops!  That was no valid number.  Try again...")
    # 把 data 放到 DataFrame 裡面
    df = pd.DataFrame(data)
    return df


tseData = getTSEStcokInfo()
otcData = getOTCStcokInfo()
allStockData = pd.concat([tseData,otcData])
allStockData.to_csv('stock.csv', index=False, encoding='utf-8-sig')
#f = open("stock.csv","w")
#w = csv.writer(f)
#with open('stock.csv','wb') as f:
#    w = unicodecsv.writer(f,encoding='utf-8-sig')
#    for row in tseData['股票代號']:
#        w.writerow(row)
#w.writerow(tseData['股票代號'])
#try:
#    w.writerow(tseData['股票名稱'])
#except UnicodeEncodeError:
#    print ("Oops!  That was no valid stock name.  Try again...")