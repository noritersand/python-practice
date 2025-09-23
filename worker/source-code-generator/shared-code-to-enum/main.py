#!/usr/bin/env python3
"""
MariaDB to Java Enum Generator
Main entry point for generating Java enum classes from database code tables
"""

import sys
from enum_generator import (
    generate_enum_from_db, 
    list_available_codes,
    get_db_connection
)


def print_banner():
    """프로그램 배너 출력"""
    print("=" * 60)
    print("📦 MariaDB to Java Enum Generator")
    print("=" * 60)


def print_menu():
    """메뉴 출력"""
    print("\n메뉴를 선택하세요:")
    print("1. 전체 코드 목록 조회")
    print("2. 특정 코드의 Enum 생성")
    print("3. 모든 코드의 Enum 일괄 생성")
    print("4. DB 연결 테스트")
    print("0. 종료")
    print("-" * 40)


def test_db_connection():
    """데이터베이스 연결 테스트"""
    try:
        conn = get_db_connection()
        print("✅ 데이터베이스 연결 성공!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return False


def show_available_codes():
    """사용 가능한 코드 목록 표시"""
    try:
        codes = list_available_codes()
        if codes:
            print("\n📋 사용 가능한 코드 목록:")
            print("-" * 60)
            print(f"{'코드':<30} {'코드명':<20} {'설명':<20}")
            print("-" * 60)
            for code in codes:
                description = code.get('description', '-') or '-'
                print(f"{code['code']:<30} {code['codeName']:<20} {description:<20}")
        else:
            print("등록된 코드가 없습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


def generate_single_enum():
    """단일 Enum 생성"""
    code_name = input("\nEnum을 생성할 코드 이름을 입력하세요: ").strip()
    if not code_name:
        print("❌ 코드 이름을 입력해주세요.")
        return
    
    try:
        enum_code = generate_enum_from_db(code_name, save_to_file=True)
        print("\n📝 생성된 Enum 코드:")
        print("-" * 60)
        print(enum_code)
        print("-" * 60)
    except Exception as e:
        print(f"❌ Enum 생성 실패: {e}")


def generate_all_enums():
    """모든 코드에 대한 Enum 일괄 생성"""
    try:
        codes = list_available_codes()
        if not codes:
            print("생성할 코드가 없습니다.")
            return
        
        success_count = 0
        fail_count = 0
        
        print(f"\n총 {len(codes)}개의 Enum을 생성합니다...")
        print("-" * 60)
        
        for code in codes:
            code_name = code['code']
            try:
                generate_enum_from_db(code_name, save_to_file=True)
                success_count += 1
                print(f"✅ {code_name} -> 성공")
            except Exception as e:
                fail_count += 1
                print(f"❌ {code_name} -> 실패: {e}")
        
        print("-" * 60)
        print(f"\n📊 결과: 성공 {success_count}개, 실패 {fail_count}개")
        
    except Exception as e:
        print(f"❌ 일괄 생성 중 오류 발생: {e}")


def main():
    """메인 함수"""
    print_banner()
    
    # 초기 DB 연결 테스트
    print("\n🔌 데이터베이스 연결 확인 중...")
    if not test_db_connection():
        print("\n⚠️  db.py 파일의 설정을 확인해주세요.")
        return
    
    while True:
        print_menu()
        choice = input("선택: ").strip()
        
        if choice == '0':
            print("\n👋 프로그램을 종료합니다.")
            break
        elif choice == '1':
            show_available_codes()
        elif choice == '2':
            generate_single_enum()
        elif choice == '3':
            generate_all_enums()
        elif choice == '4':
            test_db_connection()
        else:
            print("❌ 올바른 메뉴를 선택해주세요.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1)
