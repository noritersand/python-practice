# MariaDB to Java Enum Generator

MariaDB의 코드 테이블 데이터를 Java Enum 클래스로 자동 생성하는 Python 프로그램입니다.

## 📋 기능

- MariaDB의 `code`와 `code_item` 테이블에서 데이터를 읽어 Java Enum 생성
- 플레이스홀더 방식으로 수정 가능한 템플릿 생성
- 단일 코드 또는 전체 코드 일괄 변환 지원
- 생성된 Enum에 유틸리티 메소드 자동 추가 (`fromLabel()`, `valueOfSafe()`)

## 🚀 설치

### 1. 필수 패키지 설치

```bash
pip install pymysql
```

### 2. 데이터베이스 설정

`db.py` 파일을 열어 MariaDB 연결 정보를 수정합니다:

```python
DB_CONFIG = {
    'mysql': {
        'host': 'localhost',      # MariaDB 서버 주소
        'port': 3306,              # 포트 번호
        'user': 'your_username',   # 사용자명
        'password': 'your_password', # 비밀번호
        'database': 'your_database', # 데이터베이스명
        'charset': 'utf8mb4'
    }
}
```

## 📁 파일 구조

```
.
├── main.py           # 메인 실행 파일
├── enum_generator.py # Enum 생성 로직
├── db.py            # 데이터베이스 설정
├── README.md        # 설명서
└── output/          # 생성된 Java 파일 저장 디렉토리
    └── *.java
```

## 💻 사용 방법

### 프로그램 실행

```bash
python main.py
```

### 메뉴 옵션

1. **전체 코드 목록 조회**: 데이터베이스의 모든 코드 확인
2. **특정 코드의 Enum 생성**: 선택한 코드만 변환
3. **모든 코드의 Enum 일괄 생성**: 전체 코드를 한 번에 변환
4. **DB 연결 테스트**: 데이터베이스 연결 상태 확인
0. **종료**: 프로그램 종료

## 📊 데이터베이스 스키마

### code 테이블
```sql
CREATE TABLE code (
    code VARCHAR(100) PRIMARY KEY,
    codeName VARCHAR(100),
    description TEXT,
    creator INT,
    updater INT
);
```

### code_item 테이블
```sql
CREATE TABLE code_item (
    code VARCHAR(100),
    codeKey VARCHAR(200),
    codeValue VARCHAR(200),
    description TEXT,
    sortOrder INT,
    creator INT,
    updater INT
);
```

## 🔄 변환 규칙

### 클래스명 변환
- 모든 코드는 `ChangeThisTypeName`으로 생성됨
- 개발자가 직접 의미있는 이름으로 수정 필요

### Enum 상수명 변환
- `CHANGE_THIS_FIELD_NAME1`, `CHANGE_THIS_FIELD_NAME2`, ... 형식으로 생성
- 개발자가 직접 의미있는 이름으로 수정 필요

## 📝 생성되는 Java 코드 예시

```java
/**
 * 등록자유형코드
 * TODO: Change class name from 'ChangeThisTypeName' to appropriate name
 */
public enum ChangeThisTypeName {
    CHANGE_THIS_FIELD_NAME1("등록자유형코드.admin관리자"),
    CHANGE_THIS_FIELD_NAME2("등록자유형코드.biz관리자"),
    CHANGE_THIS_FIELD_NAME3("등록자유형코드.회원"),
    CHANGE_THIS_FIELD_NAME4("등록자유형코드.사용자");
    
    private final String label;
    
    ChangeThisTypeName(String label) {
        this.label = label;
    }
    
    public String label() {
        return label;
    }
    
    /**
     * label이 일치하는 enum 반환
     */
    public static ChangeThisTypeName fromLabel(String label) {
        ChangeThisTypeName[] values = ChangeThisTypeName.values();
        for (ChangeThisTypeName ele : values) {
            if (ele.label().equals(label)) {
                return ele;
            }
        }
        return null;
    }
    
    /**
     * enum 상수명이 일치하는 enum 반환
     */
    public static ChangeThisTypeName valueOfSafe(String name) {
        try {
            return ChangeThisTypeName.valueOf(name);
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}
```

⚠️ **생성된 코드 수정 필요**:
1. `ChangeThisTypeName` → 실제 의미있는 클래스명으로 변경 (예: `CreatorTypeCode`)
2. `CHANGE_THIS_FIELD_NAME1~4` → 실제 의미있는 필드명으로 변경 (예: `ADMIN_MANAGER`, `BIZ_MANAGER`, `MEMBER`, `DIGITAL_ID`)

## ⚠️ 주의사항

1. **데이터베이스 권한**: 실행 사용자는 `code`와 `code_item` 테이블에 대한 SELECT 권한이 필요합니다
2. **문자 인코딩**: 한글 처리를 위해 `utf8mb4` 인코딩 사용을 권장합니다
3. **파일 덮어쓰기**: 동일한 이름의 Java 파일이 있을 경우 덮어쓰기됩니다
4. **생성 파일명**: 한글 코드명 그대로 파일명으로 사용됩니다 (예: `등록자유형코드.java`)

## 🛠 문제 해결

### DB 연결 실패
- `db.py`의 연결 정보 확인
- MariaDB 서버 실행 상태 확인
- 방화벽 설정 확인

### 한글 깨짐
- 데이터베이스와 테이블의 문자셋이 `utf8mb4`인지 확인
- Python 파일 인코딩이 UTF-8인지 확인
