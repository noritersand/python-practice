import urllib.request
from bs4 import BeautifulSoup

url = 'https://kr.iherb.com/search?kw=21st%20century'
request = urllib.request.Request(url)
request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0')
html = urllib.request.urlopen(request).read()
soup = BeautifulSoup(html, 'html.parser')

address = soup.find_all(class_='absolute-link product-link')

for i in address:
    print(i.attrs['href'])
    print()

# GET /search?kw=21st%20century HTTP/3
# Host: kr.iherb.com
# 'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
# Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
# Accept-Encoding: gzip, deflate, br
# DNT: 1
# Alt-Used: kr.iherb.com
# Connection: keep-alive
# Cookie: ihr-temse=cc=KR&expires=13%20Mar%202022%2004:41:33Z; ih-preference=store=0&country=KR&language=ko-KR&currency=KRW; iher-pref1=storeid=0&sccode=KR&lan=ko-KR&scurcode=KRW&wp=2; ih-experiment=e30=; __cf_bm=tT_oVEzE2yRyKTcq3hwqQV4mNRAgS6znOrfsAlNypdQ-1647142891-0-AaZ1sTg1pCRFQGdlF1e+jqelYAq7m2NXlYfmiocqeobgu9ji5//bm74W7bwOSivRVe9buKEAmexemp8igUW8fxE8CuqS57drsbGNpKOOHWsD; ih-cc-pref=eyJmdW5jdGlvbmFsIjowLCJhbmFseXRpY3MiOjB9; notice_behavior=implied,eu; ih-hp-vp=01; __cfruid=c1845b7647bbf9e3c708b45842e33e25ba1f1329-1647142893
# Upgrade-Insecure-Requests: 1
# Sec-Fetch-Dest: document
# Sec-Fetch-Mode: navigate
# Sec-Fetch-Site: none
# Sec-Fetch-User: ?1
# TE: trailers