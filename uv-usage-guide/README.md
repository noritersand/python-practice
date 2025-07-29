# uv-usage-guide

파이썬의 초고속 패키지 매니저 uv 사용 가이드.

## uv 설치

choco로 설치함

```bash
# 관리자 권한 획득 후
choco install uv
```

## uv 프로젝트 생성

```bash
uv init
```

## 의존성 추가하기

```bash
uv add PACKAGE_NAME
```

## 의존성 설치하기

`.venv` 디렉터리가 없으면 실행할 것

```bash
uv sync
```

## 파이썬 스크립트 실행

```bash
uv run FILE_NAME
```
