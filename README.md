# python-lab

python lab.

#### environments

- Python 3.8.1

## 파이썬 설치

[다운로드 링크](https://www.python.org/downloads/)

## 특정 모듈 설치

pip나 easy_install 실행파일이 있는 경로로 이동 후

```py
> pip install 모듈명
```

```py
> easy_install 모듈명
```

pip는 윈도우10 + 기본 설치일 경우 `C:\Users\윈도우유저명\AppData\Local\Programs\Python\Python38-32\Scripts` 요딴 경로에 있다.

가령 BeautifulSoup4을 사용하려면 일단 모듈 설치:

```py
> pip install beautifulsoup4
```

이 후 다음처럼 작성한다:

```py
from bs4 import BeautifulSoup

html_doc = '<div></div>'
# print(html_doc)

soup = BeautifulSoup(html_doc, 'html.parser')
```

## 프로그램 파일 작성

파이썬 설치 시 딸려오는 IDLE 편집기를 사용하거나 별도의 에디터로 직접 작성한다. 파이썬 파일의 확장명은 보통 `py`로 한다.

## 프로그램 파일 실행

파일이 있는 경로에서 `py`로 실행:

```py
> py test.py
```

IDLE 편집기로 파일을 열고 있는 상태라면 `f5`로 즉시 실행할 수 있다.
