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

# 브라우저가 닫히지 않도록 설정
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.implicitly_wait(2) # 엘리먼트를 찾을 때 최대 2초 대기

# 빈 페이지 열기
driver.get('about:blank')

# JavaScript로 동적 폼 생성 및 제출
script = """
// 폼 엘리먼트 생성
let form = document.createElement('form');
form.method = 'POST';
form.action = 'https://example.com/index.do';

let input1 = document.createElement('input');
input1.type = 'text';
input1.name = 'type';
input1.value = 'P'
form.appendChild(input1);

let input2 = document.createElement('input');
input2.type = 'text';
input2.name = 'classCode';
input2.value = 'GO'
form.appendChild(input2);

let input3 = document.createElement('input');
input3.type = 'text';
input3.name = 'korName';
input3.value = '이뿅뿅'
form.appendChild(input3);

let input4 = document.createElement('input');
input4.type = 'text';
input4.name = 'birthDate';
input4.value = '20010203'
form.appendChild(input4);

let input5 = document.createElement('input');
input5.type = 'text';
input5.name = 'gender';
input5.value = 'm'
form.appendChild(input5);

// body에 폼 추가
document.body.appendChild(form);

// 폼 제출
form.submit();
"""

# JavaScript 실행
driver.execute_script(script)

# 제출 후 응답 확인을 위해 잠시 대기
import time
time.sleep(5)  # 서버 응답 확인할 시간

# 현재 URL 또는 페이지 소스 출력 (확인용)
print(driver.current_url)
print(driver.page_source)

exit()
