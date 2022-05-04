import requests
from bs4 import BeautifulSoup

keyword = "apple ipad"
url = "https://slickdeals.net/newsearch.php?src=SearchBarV2&q={}&searcharea=deals&searchin=first".format(keyword)
r = requests.get(url)
bs = BeautifulSoup(r.content, "lxml")
divs = bs.select("div.resultRow")

for d in divs:
	image = d.select("div.dealImg > a")[0]
	rimages = image.select("img.lazyimg")[0]
	image1 = rimages.get("data-original")
	if rimages is None:
		continue
	print(image1)
