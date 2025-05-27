import cx_Oracle

# Oracle 연결 정보
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
dsn = 'YOUR_HOST:YOUR_PORT/YOUR_SERVICE_NAME'  # 예: 'localhost:1521/ORCLPDB1'

# 파일 경로
query_file = 'query.sql'
output_file = 'member-ids'

try:
    # 쿼리 파일에서 SQL 읽기
    with open(query_file, 'r', encoding='utf-8') as f:
        query = f.read().strip()

    # Oracle DB 연결
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()

    # 쿼리 실행
    cursor.execute(query)

    # 결과를 파일에 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        for row in cursor:
            f.write(f"{row[0]}\n")

    print(f"쿼리 결과가 '{output_file}' 파일에 저장되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
