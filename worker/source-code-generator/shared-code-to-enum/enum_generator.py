"""
Enum Generator Module
Generates Java enum classes from MariaDB code tables
"""

import re
from typing import List, Dict, Tuple, Optional
import pymysql
from db import DB_CONFIG, DB_TYPE


def get_db_connection():
    """데이터베이스 연결 생성"""
    config = DB_CONFIG[DB_TYPE]
    return pymysql.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        charset=config['charset'],
        cursorclass=pymysql.cursors.DictCursor
    )


def fetch_code_data(code_name: str) -> Tuple[Dict, List[Dict]]:
    """
    특정 코드의 데이터를 가져옴
    
    Args:
        code_name: 조회할 코드 이름
        
    Returns:
        (code 정보, code_item 리스트) 튜플
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # code 테이블 조회
            cursor.execute(
                "SELECT * FROM code WHERE code = %s",
                (code_name,)
            )
            code_info = cursor.fetchone()
            
            # code_item 테이블 조회
            cursor.execute(
                "SELECT * FROM code_item WHERE code = %s ORDER BY sortOrder",
                (code_name,)
            )
            code_items = cursor.fetchall()
            
            return code_info, code_items
    finally:
        conn.close()


def to_enum_name(code_key: str, code_value: str, index: int) -> str:
    """
    codeKey를 Java enum 이름으로 변환
    
    Args:
        code_key: 원본 코드키
        code_value: 코드 값
        index: 순번 (1부터 시작)
        
    Returns:
        변환된 enum 이름 (CHANGE_THIS_FIELD_NAME 형식)
    """
    return f"CHANGE_THIS_FIELD_NAME{index}"


def to_class_name(code_name: str) -> str:
    """
    코드 이름을 Java 클래스명으로 변환
    
    Args:
        code_name: 원본 코드 이름
        
    Returns:
        수정 가능한 플레이스홀더 클래스명
    """
    return "ChangeThisTypeName"


def generate_enum_class(code_name: str, code_items: List[Dict]) -> str:
    """
    Java enum 클래스 코드 생성
    
    Args:
        code_name: 코드 이름
        code_items: 코드 아이템 리스트
        
    Returns:
        생성된 Java enum 코드
    """
    class_name = to_class_name(code_name)
    
    # Javadoc 생성 - 원본 코드명 포함
    javadoc = f"""/**
 * {code_name}
 * TODO: Change class name from 'ChangeThisTypeName' to appropriate name
 */"""
    
    # Enum 상수 생성
    enum_constants = []
    for index, item in enumerate(code_items, 1):
        code_key = item['codeKey']
        code_value = item['codeValue']
        enum_name = to_enum_name(code_key, code_value, index)
        
        enum_constants.append(f'    {enum_name}("{code_key}")')
    
    enum_constants_str = ',\n'.join(enum_constants) + ';'
    
    # 클래스 본문 생성
    class_body = f"""public enum {class_name} {{
{enum_constants_str}
    
    private final String label;
    
    {class_name}(String label) {{
        this.label = label;
    }}
    
    public String label() {{
        return label;
    }}
    
    /**
     * label이 일치하는 enum 반환
     */
    public static {class_name} fromLabel(String label) {{
        {class_name}[] values = {class_name}.values();
        for ({class_name} ele : values) {{
            if (ele.label().equals(label)) {{
                return ele;
            }}
        }}
        return null;
    }}
    
    /**
     * enum 상수명이 일치하는 enum 반환
     */
    public static {class_name} valueOfSafe(String name) {{
        try {{
            return {class_name}.valueOf(name);
        }} catch (IllegalArgumentException e) {{
            return null;
        }}
    }}
}}"""
    
    return f"{javadoc}\n{class_body}"


def save_enum_to_file(code_name: str, enum_code: str, output_dir: str = './output') -> str:
    """
    생성된 enum 코드를 파일로 저장
    
    Args:
        code_name: 코드 이름
        enum_code: 생성된 Java enum 코드
        output_dir: 출력 디렉토리
        
    Returns:
        저장된 파일 경로
    """
    import os
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 파일명 생성 (한글 그대로 사용하되 특수문자 제거)
    safe_filename = re.sub(r'[^\w가-힣]', '', code_name)
    file_path = os.path.join(output_dir, f"{safe_filename}.java")
    
    # 파일 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(enum_code)
    
    return file_path


def generate_enum_from_db(code_name: str, save_to_file: bool = True) -> str:
    """
    데이터베이스에서 코드를 읽어 Java enum 생성
    
    Args:
        code_name: 생성할 코드 이름
        save_to_file: 파일로 저장할지 여부
        
    Returns:
        생성된 Java enum 코드
    """
    try:
        # 데이터베이스에서 코드 정보 조회
        code_info, code_items = fetch_code_data(code_name)
        
        if not code_info:
            raise ValueError(f"코드 '{code_name}'를 찾을 수 없습니다.")
        
        if not code_items:
            raise ValueError(f"코드 '{code_name}'에 대한 아이템이 없습니다.")
        
        # Enum 클래스 생성
        enum_code = generate_enum_class(code_name, code_items)
        
        # 파일로 저장
        if save_to_file:
            file_path = save_enum_to_file(code_name, enum_code)
            print(f"✅ Enum 클래스가 생성되었습니다: {file_path}")
        
        return enum_code
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        raise


def list_available_codes() -> List[str]:
    """
    사용 가능한 모든 코드 목록 조회
    
    Returns:
        코드 이름 리스트
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT code, codeName, description FROM code ORDER BY code")
            codes = cursor.fetchall()
            return codes
    finally:
        conn.close()