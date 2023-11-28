from bs4 import BeautifulSoup

html_doc = '''
  <!doctype html>
  <html>
  <head>
      <title>Example Domain</title>
      <meta charset="utf-8" />
      <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <style type="text/css">
      body { background-color: #f0f0f2; margin: 0; padding: 0; font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif; }
      </style>
  </head>
  <body>
  <div>
      <h1>Example Domain</h1>
      <p class="dormammu">qwer</p>
      <p><a href="https://www.iana.org/domains/example">More information...</a></p>
  </div>
  </body>
  </html>
'''
# print(html_doc)

soup = BeautifulSoup(html_doc, 'html.parser')

# subjects = soup.select('.item-subject')  #게시글 클래스 선택
# for subject in subjects:
    # print(subject.select_one('span.wr-new')['class'])

print(soup.find_all('p'))
print(soup.find_all('p', class_="dormammu"))

