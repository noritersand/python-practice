import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

host = 'http://localhost:7080/'

# 성공 로거 설정
success_logger = logging.getLogger('success_logger')
success_handler = logging.FileHandler('success.log', encoding='utf-8')
success_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
success_logger.addHandler(success_handler)
success_logger.setLevel(logging.INFO)

# 실패 로거 설정
fail_logger = logging.getLogger('fail_logger')
fail_handler = logging.FileHandler('fail.log', encoding='utf-8')
fail_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
fail_logger.addHandler(fail_handler)
fail_logger.setLevel(logging.ERROR)

def post_member(member_id):
    url = f'{host}members/{member_id}'
    print(f'POST 요청: {url}')
    try:
        response = requests.post(url)
        try:
            json_data = response.json()
        except Exception:
            json_data = {}

        log_message = f'memberId: {member_id}, 응답 상태 코드: {response.status_code}, 응답 본문: {response.text}'
        
        if 200 <= response.status_code < 300 and json_data.get("success") is True:
            success_logger.info(log_message)
        else:
            fail_logger.error(log_message)
        
        return log_message
    except Exception as e:
        error_message = f'memberId: {member_id}, 요청 중 오류 발생: {e}'
        fail_logger.error(error_message)
        return error_message

# 파일에서 대상 목록 읽기
with open('./targets', 'r') as f:
    member_ids = [line.strip() for line in f if line.strip()]

futures = []

with ThreadPoolExecutor(max_workers=10) as executor:
    for member_id in member_ids:
        future = executor.submit(post_member, member_id)
        futures.append(future)
        time.sleep(0.2)  # 초 단위 간격

    for future in as_completed(futures):
        print(future.result())
