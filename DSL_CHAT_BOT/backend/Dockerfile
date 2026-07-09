# Python 기반 이미지 사용
FROM python:3.10-slim

WORKDIR /app

# 의존성 복사 및 설치
ARG REQUIREMENTS_FILE=requirements.nim.txt
COPY requirements.txt requirements.nim.txt ./
RUN pip install --no-cache-dir -r "${REQUIREMENTS_FILE}"

# 소스 코드 복사
COPY . .

# API 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
