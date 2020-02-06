import requests
import urllib.request
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

old_newsflashs = []

def extract_newsflashs(old_newsflashs=[]):
    url = 'https://m.search.naver.com/search.naver?where=m_news&query=1보&sm=mtb_tnw&sort=1'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    search_result = soup.select_one('#news_result_list')
    result_list = search_result.select('.bx > .news_wrap > a')

    news_list = []
    for title_list in result_list:
        title = (title_list.get_text())
        news_link = title_list['href']

        if '코로나' in title:
            news_list.append([title, news_link])
##            print([title, news_link])

    newsflashs = []
    for news_list in result_list[:10]:
        newsflash = news_list
        print(newsflash)
        newsflashs.append(newsflash)

    new_newsflashs=[]
    for newsflash in newsflashs:
        if newsflash not in old_newsflashs:
            new_newsflashs.append(newsflash)

    return new_newsflashs

new_newsflashs = extract_newsflashs(old_newsflashs)
##if new_newsflashs:
##    for newsflash in new_newsflashs:
##        print(tuple(newsflash))


