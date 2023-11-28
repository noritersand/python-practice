from bs4 import BeautifulSoup
import requests
import codecs

base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=python"
search_term = "python"

response = requests.get(f"{base_url}{search_term}")


f = codecs.open("result.txt", "w", "utf-8") # w: write, r: read, a: append
f.write(response.text)
f.close()


if response.status_code != 200:
  print("can't request website.")
else:
  soup = BeautifulSoup(response.text, "html.parser")
  # print(soup)
  # jobs = soup.find_all('section', class_='jobs')
  jobs = soup.find_all('section', {'class': 'jobs'})
  print(len(jobs))