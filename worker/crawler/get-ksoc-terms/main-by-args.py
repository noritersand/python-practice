import argparse
import codecs
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # 자동 드라이버 관리
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from account import ACCOUNT

parser = argparse.ArgumentParser(description="아규먼트 처리 스크립트")
parser.add_argument("--no", help="종목 번호", default='2052')
parser.add_argument("--code", help="종목 코드", default='KR')
parser.add_argument("--name", help="종목 이름", default='사실이건아무거나해도상관없는값')
args = parser.parse_args()
print("args.no:", args.no)
print("args.code:", args.code)
print("args.name:", args.name)

# 브라우저가 닫히지 않도록 설정
# chrome_options = Options()
# chrome_options.add_experimental_option('detach', True)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.implicitly_wait(2) # 엘리먼트를 찾을 때 최대 2초 대기

# 로그인 페이지로 이동
driver.get('https://g1.sports.or.kr/member/login.do?retUrl=%2Findex.do')

# 아이디와 비밀번호 입력 필드 찾기
username_field = driver.find_element(By.NAME, 'userId')
password_field = driver.find_element(By.NAME, 'passwd')

# 아이디와 비밀번호 입력
username_field.send_keys(ACCOUNT['id']) # 실제 아이디
password_field.send_keys(ACCOUNT['password']) # 실제 비밀번호

# 로그인 버튼 찾고 클릭
driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

# 로그인 성공 여부 확인
try:
    success_element = driver.find_element(By.CLASS_NAME, 'inner-contents__center') # 엘리먼트를 못찾으면 에러 발생함
    # print('로그인 성공:', success_element.text)
    print('로그인 성공')
except:
    print('로그인 실패')

# driver.get('https://g1.sports.or.kr/pinfo/index/sc000.do') # 페이지 이동
driver.execute_script("movePinfo()")
time.sleep(1)

# result/ 디렉터리 생성하기
resultDir = './result/'
if not os.path.isdir(resultDir):
    os.mkdir(resultDir)

driver.execute_script(f"fnMoveClass('P', '{args.no}', '{args.code}', '{args.name}')")
time.sleep(1)

try:
    success_element = driver.find_element(By.CSS_SELECTOR, 'a[href="/pinfo/player/sc246.do"]') # 엘리먼트를 못찾으면 에러 발생함
except:
    print('개인정보처리방침 버튼 못찾음. 브라우저 종료됨')
    driver.quit()
    exit() # 스크립트 종료

driver.get('https://g1.sports.or.kr/pinfo/player/sc246.do')

content_element = driver.find_element(By.CSS_SELECTOR, 'div.intro-ex-item')

f = codecs.open(f'./{resultDir}/{args.no}-{args.code}-개인정보처리방침.html', 'w', 'utf-8')
f.write(content_element.get_attribute('innerHTML'))
f.close()

# ----- 마무-으리 -----

print('현재 주소:', driver.current_url)

# 3초 후 브라우저 종료
print('3초 후 브라우저 종료됨')
time.sleep(3)
driver.quit()
