from bs4 import BeautifulSoup
import urllib.request

url = "https://www.weather.go.kr/w/weather/forecast/mid-term.do?stnId1=108"

response = urllib.request.urlopen(url)
datas = response.read()

soup = BeautifulSoup(datas, "html.parser")

date = soup.find_all("thead")[0].find_all("tr")[0].find_all("th")[1:]
seoul = soup.find_all("tbody")[0].find_all("tr")[0]
weather = seoul.find_all(class_="wic")[1:]

tp = soup.find_all("tbody")[1].find("tr").find_all("span")[2:]

def emoji(text):
    text = text.strip()
    if text == "맑음":
        return "☀️"
    elif text == "구름많음":
        return "⛅"
    elif text == "흐림":
        return "☁️"
    elif text == "비":
        return "🌧️"
    elif text == "눈":
        return "❄️"
    else:
        return text

def color(txt, code):
    return f"\033[{code}m{txt}\033[0m"


print("-" * 40)

for i in range(7):
    day = date[i].get_text(strip=True)[:2]
    low = tp[i * 2].text.strip()
    high = tp[i * 2 + 1].text.strip()

    header = color(f"[ {day}th ]", "1;33")
    temp = color(f"🌡️ {low}°C  ~  {high}°C", "1;32")

    print(header)
    print(temp)

    if i < 4:
        am = emoji(weather[i * 2].text)
        pm = emoji(weather[i * 2 + 1].text)
    else:
        am = pm = emoji(weather[i + 4].text)

    print(f"  오전: {am}   오후: {pm}")
    print("-" * 40)
