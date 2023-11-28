import time
import requests
import certifi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # 자동 드라이버 관리
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.alert import Alert

def handleAlert():
    try:
        alert = Alert(driver)  # 현재 alert 가져오기
        print("Alert Text:", alert.text)  # 경고창 메시지 확인
        alert.accept()  # 확인(OK) 클릭 (또는 alert.dismiss()로 취소)
        print("Alert 닫음")
        goToAssociation()
    except NoAlertPresentException:
        print("Alert 없음")

def goToAssociation():
    # driver.get('https://g1.sports.or.kr/pinfo/index/sc000.do') # 페이지 이동
    driver.execute_script("movePinfo()")
    driver.implicitly_wait(5) # 최대 5초 대기
    time.sleep(1)
    driver.execute_script("fnMoveClass('P','2052','KR','가라테')")
    driver.implicitly_wait(5) # 최대 5초 대기

# Chrome 옵션, 드라이버 설정
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)  # 브라우저가 닫히지 않도록 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 로그인 페이지로 이동
driver.get('https://g1.sports.or.kr/member/login.do?retUrl=%2Findex.do')

# 아이디와 비밀번호 입력 필드 찾기 (HTML 구조에 따라 수정 필요)
username_field = driver.find_element(By.NAME, 'userId')
password_field = driver.find_element(By.NAME, 'passwd')

# 아이디와 비밀번호 입력
username_field.send_keys('fixalot') # 실제 아이디
password_field.send_keys('Qwepoi12sposor3$') # 실제 비밀번호

# 로그인 버튼 찾고 클릭 (HTML 구조에 따라 수정 필요)
login_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
if login_button is not None:
    print('로그인 버튼 찾음')

login_button.click()

driver.implicitly_wait(5) # 최대 5초 대기

# 로그인 성공 여부 확인 (예: 특정 요소가 나타나는지)
try:
    success_element = driver.find_element(By.CLASS_NAME, 'inner-contents__center') # 엘리먼트를 못찾으면 에러 발생함
    # print('로그인 성공:', success_element.text)
    print('로그인 성공')
except:
    print('로그인 실패')

goToAssociation()
time.sleep(1)

driver.get('https://g1.sports.or.kr/pinfo/player/sc246.do')
driver.implicitly_wait(5) # 최대 5초 대기

content_element = driver.find_element(By.CLASS_NAME, 'content-body intro')
print(content_element.get_attribute('innerHTML'))

# element_tmpFrm = driver.find_element(By.NAME, 'tmpFrm')
# if element_tmpFrm is not None:
#     driver.get('https://g1.sports.or.kr/pinfo/index/sc000.do') # 페이지 이동
#     driver.implicitly_wait(5) # 최대 5초 대기

# ----- 마무-으리 -----

print('현재 주소:', driver.current_url)

# 5초 후 브라우저 종료
# time.sleep(5)
# driver.quit()
