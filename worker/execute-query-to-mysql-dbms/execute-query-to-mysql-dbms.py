import mysql.connector

from db import datasource
'''
datasource 딕셔너리를 db.py에 정의해야 정상 작동함
예시: 
datasource = {
    'host': "example.com",  # 데이터베이스 호스트
    'port': 1234,
    'user': "username",  # 데이터베이스 사용자 이름
    'password': "passwoooooooord",  # 데이터베이스 비밀번호
    'database': "schemaname"  # 데이터베이스 이름
}
'''

# SQL 쿼리를 파일에서 읽어옵니다.
with open('query.sql', 'r') as file:
    query = file.read()

# 데이터베이스에 접속
conn = mysql.connector.connect(**datasource)

# 커서 객체 생성
cursor = conn.cursor()
# SQL 쿼리 실행
cursor.execute(query)
# 결과셋
rows = cursor.fetchall();

# 대충 출력하기
def printNormal(rows):
    rst = ''
    for row in rows:
        # rst += str(row[0]) 
        # rst += ', ' 
        rst += '"' + str(row[1]) + '",'
        rst += '\n'
    rst = rst[:-2] # 마지막 문자 두 개 지우기
    return rst

# Java Map으로
def printMap(rows):
    rst = ''
    for row in rows:
        rst += 'map = new HashMap<>();'
        rst += 'map.put("no", "' + str(row[0]) + '");'
        rst += 'map.put("name", "' + str(row[1]) + '");'
        rst += 'list.add(map);'
        rst += '\n'
    return rst

# 결과를 파일에 쓰기
with open('output1', 'w', encoding='UTF-8') as file:
    file.write(printNormal(rows))

# 결과를 파일에 쓰기
with open('output2', 'w', encoding='UTF-8') as file:
    file.write(printMap(rows))

# 커서와 연결 종료
cursor.close()
conn.close()
