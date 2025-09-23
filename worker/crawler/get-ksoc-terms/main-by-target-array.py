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
from terms_target_list import terms_target_list
from account import ACCOUNT

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

# output/ 디렉터리 생성하기
outputDir = './output/'
if not os.path.isdir(outputDir):
    os.mkdir(outputDir)

def write_file(codeNo, code, name, content):
    f = codecs.open(f'./{outputDir}/{codeNo}-{code}-{name}.html', 'w', 'utf-8')
    f.write(content)
    f.close()

for target in terms_target_list:
    driver.execute_script(f"fnMoveClass('P', '{target['codeNo']}', '{target['code']}', '{target['name']}')")
    time.sleep(1)
    
    try:
        success_element = driver.find_element(By.CSS_SELECTOR, 'a[href="/pinfo/player/sc246.do"]')
    except:
        print(f'{target['name']} 개인정보처리방침 버튼 못찾음. 빈 파일 생성함')
        write_file(target['codeNo'], target['code'], target['name'], '')
        driver.get('https://g1.sports.or.kr/pinfo/index/sc000.do')
        continue

    driver.get('https://g1.sports.or.kr/pinfo/player/sc246.do')

    content_element = driver.find_element(By.CSS_SELECTOR, 'div.intro-ex-item')

    write_file(target['codeNo'], target['code'], target['name'], content_element.get_attribute('innerHTML'))

    driver.get('https://g1.sports.or.kr/pinfo/index/sc000.do')

# ----- 마무-으리 -----

# 3초 후 브라우저 종료
print('3초 후 브라우저 종료됨')
time.sleep(3)
driver.quit()
