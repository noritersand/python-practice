from bs4 import BeautifulSoup
import requests

url = f"https://example.com"
request = requests.get(url, headers={"User-Agent": "Kimchi"})
if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")
    print(soup)

else:
    print("Can't get page")

