import pandas as pd
import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import openpyxl

def getLinks(pageUrl) :

    global pages
    j=2
    for num in range(1, 2):          # A-1,A-2... 이 메뉴를 돌아다님
        html1 = ("http://www.steeland.net/shop_contents/myboard_list.htm?page=1&myboard_code=sub2_" + str(num))
        for num1 in range(1, 2):   #  페이지를 돌아다님.
            html2 = html1.replace("page=1", "page=" + str(num1))
            print(html2)        #접속한 페이지 주소 표시
            html = urlopen(html2)
            bsObj = BeautifulSoup(html,"html.parser")
            company_Info_list=[]
            company_Info_list = bsObj.select(
                '#container01 > div.cont.sub > div.sb1_2.sb2_1 > div.sc2 > div.company_list > ul > li > div')
            # print(company_Info_list.len)
            print(company_Info_list)
            print(type(company_Info_list))
            print('---------------------------')
            company_Info_list = bsObj.find_all(
                '#container01 > div.cont.sub > div.sb1_2.sb2_1 > div.sc2 > div.company_list > ul > li > div')
            # print(company_Info_list.len)
            print(type(company_Info_list))
            print(company_Info_list)
            print('---------------------------')
            # print(bsObj)
            data=[]
            for obj in company_Info_list:
                # print(obj.a.attrs)
                # print(obj.a['data-title'],obj.a.get('data-name03'),obj.a.get('data-name04'),obj.a.get('data-name05'),obj.a.get('data-name06'),obj.a.get('data-name07'),obj.a.get('data-name08'),obj.a.get('data-name09'))
                data=obj.a.get('data-title'),obj.a.get('data-name03'),obj.a.get('data-name04'),obj.a.get('data-name05'),obj.a.get('data-name06'),obj.a.get('data-name07'),obj.a.get('data-name08'),obj.a.get('data-name09')

getLinks(" ")
