# python-practice

파이썬 테스트용 저장소.

#### environments

- Python 3.x.x


## 파이썬 설치

~~[다운로드 링크](https://www.python.org/downloads/)~~ Windows면 Chocolatey로 설치:

```bash
choco install python
```


## 패키지 설치

~~pip로 설치함. pip는 설치 기본 경로는 `C:\Users\윈도우유저명\AppData\Local\Programs\Python\Python38-32\Scripts` 요런식~~

uv로 설치함:

```bash
uv init
uv add PACKAGE_NAME
```


## 스크립트 실행

파일이 있는 경로에서 ~~`py`로~~ `uv`로 실행:

```bash
uv run test.py
```
