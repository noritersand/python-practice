import requests
from bs4 import BeautifulSoup

# 세션을 사용해 로그인 상태 유지
session = requests.Session()

# 로그인 정보
login_url = 'https://example.com/login'  # 실제 로그인 URL로 변경
login_data = {
    'username': 'your_username',  # 실제 사용자 이름
    'password': 'your_password'   # 실제 비밀번호
}

# 로그인 요청
response = session.post(login_url, data=login_data)

# 로그인 성공 여부 확인 (상태 코드 200이면 성공)
if response.status_code == 200:
    print("로그인 성공")
else:
    print("로그인 실패")
    exit()

# POST 요청으로 이동할 페이지
target_url = 'https://example.com/target_page'  # 실제 타겟 URL로 변경
post_data = {
    'key1': 'value1',  # 필요한 POST 데이터 (사이트마다 다름)
    'key2': 'value2'
}

# POST 요청 보내기
target_response = session.post(target_url, data=post_data)

# 버튼 클릭 시뮬레이션 (사이트가 JavaScript로 동작하지 않는다고 가정)
soup = BeautifulSoup(target_response.text, 'html.parser')

# 버튼을 찾아서 해당 URL로 이동 (예: 버튼이 링크를 포함한 경우)
button_link = soup.find('a', {'class': 'button-class'})  # 버튼의 실제 클래스나 속성으로 변경
if button_link and 'href' in button_link.attrs:
    final_url = button_link['href']
    final_response = session.get(final_url)
    
    # 최종 페이지에서 데이터 긁어오기
    final_soup = BeautifulSoup(final_response.text, 'html.parser')
    content = final_soup.find('div', {'class': 'content-class'})  # 긁어올 내용의 실제 태그와 클래스
    
    if content:
        print("긁어온 내용:", content.text.strip())
    else:
        print("내용을 찾을 수 없음")
else:
    print("버튼을 찾을 수 없음")

# 세션 종료
session.close()
