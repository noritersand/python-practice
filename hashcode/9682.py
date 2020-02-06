import re
import requests
import urllib.request
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Process

sched = BlockingScheduler()

old_links_1 = []

def extract_links_1(old_links_1=[]):
    url_1 = 'https://m.search.naver.com/search.naver?where=m_news&query=속보&sm=mtb_tnw&sort=1'
    req_1 = requests.get(url_1)
    html_1 = req_1.text
    soup_1 = BeautifulSoup(html_1, 'html.parser')

    search_result_1 = soup_1.select_one('#news_result_list')
    news_list_1 = search_result_1.select('.bx > .news_wrap > a')

    links_1 = []
    for news_1 in news_list_1[:10]:
        link_1 = (news_1.get_text())
        links_1.append(link_1)

    new_links_1=[]
    for link_1 in links_1:
        if link_1 not in old_links_1:
            new_links_1.append(link_1)

    return new_links_1

def send_links_1():
    global old_links_1
    new_links_1 = extract_links_1(old_links_1)
    if new_links_1:
        for link_1 in new_links_1:
            print('[속보]','\n'+link_1)
    else:
        pass
    old_links_1 += new_links_1.copy()
    old_links_1 = list(set(old_links_1))

old_links_2 = []

def extract_links_2(old_links_2=[]):
    url_2 = 'https://m.search.naver.com/search.naver?where=m_news&query=1보&sm=mtb_tnw&sort=1'
    req_2 = requests.get(url_2)
    html_2 = req_2.text
    soup_2 = BeautifulSoup(html_2, 'html.parser')

    search_result_2 = soup_2.select_one('#news_result_list')
    news_list_2 = search_result_2.select('.bx > .news_wrap > a')

    links_2 = []
    for news_2 in news_list_2[:10]:
        link_2 = (news_2.get_text())
        links_2.append(link_2)

    new_links_2=[]
    for link_2 in links_2:
        if link_2 not in old_links_2:
            new_links_2.append(link_2)

    return new_links_2

def send_links_2():
    global old_links_2
    new_links_2 = extract_links_2(old_links_2)
    if new_links_2:
        for link_2 in new_links_2:
            print('[1보]','\n'+link_2)
    else:
        pass
    old_links_2 += new_links_2.copy()
    old_links_2 = list(set(old_links_2))

old_links_3 = []

def extract_links_3(old_links_3=[]):
    url_3 = 'https://m.search.naver.com/search.naver?where=m_news&query=2보&sm=mtb_tnw&sort=1'
    req_3 = requests.get(url_3)
    html_3 = req_3.text
    soup_3 = BeautifulSoup(html_3, 'html.parser')

    search_result_3 = soup_3.select_one('#news_result_list')
    news_list_3 = search_result_3.select('.bx > .news_wrap > a')

    links_3 = []
    for news_3 in news_list_3[:10]:
        link_3 = (news_3.get_text())
        links_3.append(link_3)

    new_links_3=[]
    for link_3 in links_3:
        if link_3 not in old_links_3:
            new_links_3.append(link_3)

    return new_links_3

def send_links_3():
    global old_links_3
    new_links_3 = extract_links_3(old_links_3)
    if new_links_3:
        for link_3 in new_links_3:
            print('[2보]','\n'+link_3)
    else:
        pass
    old_links_3 += new_links_3.copy()
    old_links_3 = list(set(old_links_3))

def sched_process(): 
    send_links_1()
    send_links_2()
    send_links_3()

if __name__ == '__main__':
    p = Process(target=sched_process, args=())
    p.start()
    p.join()

sched_process

sched.add_job(sched_process, 'interval', seconds=5)

sched.start()
