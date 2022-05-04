import argparse

parser = argparse.ArgumentParser(description="아규먼트 처리 스크립트")

# 인자 추가
parser.add_argument("first", help="첫 번째 인자")  # 필수 인자
parser.add_argument("--second", help="선택적 두 번째 인자", default="default")  # 선택 인자
parser.add_argument("-n", "--number", type=int, help="숫자 인자", required=False)  # 타입 지정 가능

# 인자 파싱
args = parser.parse_args()

# 인자 사용
print("첫 번째 인자:", args.first)
print("두 번째 인자:", args.second)
print("숫자 인자:", args.number)
