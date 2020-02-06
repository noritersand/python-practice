from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time

dict_keyword = {}

def daum():

    browser = webdriver.Chrome("C:/dev/chromedriver/chromedriver.exe")
    browser.get("https://www.naver.com")

    html = browser.page_source

    soup = BeautifulSoup(driver.page_source, "html.parser")


    search_word = soup.select("#sp_nws_all1 > dl > dt")

##    print(soup)
##    print(soup.select("#PM_ID_ct"))
          
    for i in search_word:
        title = i.find("a").attrs['href']
        link = "https://www.daum.net" + i.find("a")["href"]
        dict_keyword[title.text] = title.get('href')

    #return dict_keyword
    print(dict_keyword)

daum()
