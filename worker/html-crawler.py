from bs4 import BeautifulSoup
import requests

url = "https://www.darkestdungeon.com/darkest-dungeon/media"
request = requests.get(url, headers={"User-Agent": "Kimchi"})
if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")
    # print(soup)
    imgs = soup.find_all('img')
    # print(type(imgs))
    srcs = []
    for img in imgs:
        srcs.append(img['src'])

    print(srcs)

else:
    print("Can't get page")

