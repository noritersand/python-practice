import requests
from bs4 import BeautifulSoup

url = "https://toss.im/"

res = requests.get(url)

res.raise_for_status

soup = BeautifulSoup(res.text, "lxml")

toss = soup.find("li", attrs={"class":"p-navbar__item"})
print(toss.find_next_siblings("li"))
