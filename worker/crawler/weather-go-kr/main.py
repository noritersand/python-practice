from bs4 import BeautifulSoup
import urllib.request

url = "https://www.weather.go.kr/w/weather/forecast/mid-term.do?stnId1=108"

response = urllib.request.urlopen(url)
xml = response.read()

soup = BeautifulSoup(xml, "html.parser")

seoul = soup.find_all("tbody")[0].find_all("tr")[0]
datas = seoul.find_all(class_="wic")[1:]

for item in datas:
    print(f"{item.text}")
