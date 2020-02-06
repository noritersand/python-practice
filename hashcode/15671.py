from bs4 import BeautifulSoup

html_doc = '<a id="pickme" href="https://example.com">나를 찾아줘요 예에</a>'
soup = BeautifulSoup(html_doc, 'html.parser')
ele = soup.select_one('#pickme')

print(ele['href'])
