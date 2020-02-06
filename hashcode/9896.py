import requests 

url = 'https://finance.naver.com/item/board.nhn?code=000020&page=1'
req = requests.get(url)
html = req.text
print(html)
