---
date: 2026-02-02
tags:
  - tech
  - modal
  - cheatsheet
  - reference
parent: "[[README]]"
---

# Modal 치트시트

> [[05-projects|이전: 실전 프로젝트]] | [[README|목차]]

빠른 참조를 위한 Modal 치트시트입니다.

---

## 설치 및 인증

```bash
# 설치
pip install modal

# 인증 (브라우저 열림)
modal setup

# 버전 확인
modal --version
```

---

## CLI 명령어

```bash
# 실행
modal run app.py              # 앱 실행 (일회성)
modal serve app.py            # 로컬 개발 서버 (핫 리로드)
modal deploy app.py           # 프로덕션 배포

# 관리
modal app list                # 배포된 앱 목록
modal app stop <name>         # 앱 중지
modal app logs <name>         # 로그 보기

# 디버깅
modal shell app.py            # 컨테이너 쉘 접속

# Volume
modal volume list             # Volume 목록
modal volume ls <name>        # Volume 내용
modal volume get <name> /remote ./local  # 다운로드
modal volume put <name> ./local /remote  # 업로드
```

---

## 기본 앱 구조

```python
import modal

app = modal.App("my-app")

@app.function()
def my_function():
    return "Hello!"

@app.local_entrypoint()
def main():
    result = my_function.remote()
    print(result)
```

---

## Function 데코레이터 옵션

```python
@app.function(
    cpu=1.0,                    # CPU 코어 수
    memory=512,                 # 메모리 (MB)
    timeout=300,                # 타임아웃 (초)
    retries=3,                  # 재시도 횟수
    gpu="T4",                   # GPU 종류
    image=custom_image,         # 커스텀 이미지
    secrets=[...],              # Secret 목록
    volumes={"/data": vol},     # Volume 마운트
    concurrency_limit=10,       # 동시 실행 제한
    schedule=modal.Cron("..."), # 스케줄링
)
def my_function():
    pass
```

---

## GPU 옵션

```python
# GPU 종류
@app.function(gpu="T4")        # NVIDIA T4 (16GB)
@app.function(gpu="L4")        # NVIDIA L4 (24GB)
@app.function(gpu="A10G")      # NVIDIA A10G (24GB)
@app.function(gpu="A100")      # NVIDIA A100 (40GB)
@app.function(gpu="A100-80GB") # NVIDIA A100 (80GB)
@app.function(gpu="H100")      # NVIDIA H100 (80GB)

# 여러 GPU
@app.function(gpu="A100:2")    # A100 2개
```

---

## Image 설정

```python
# 기본 이미지
image = modal.Image.debian_slim()

# Python 버전 지정
image = modal.Image.debian_slim(python_version="3.11")

# pip 패키지 설치
image = modal.Image.debian_slim().pip_install(
    "torch",
    "transformers",
    "pandas"
)

# 시스템 패키지 설치
image = image.apt_install("ffmpeg", "libsm6")

# 쉘 명령 실행
image = image.run_commands("echo 'setup'")

# 환경 변수 설정
image = image.env({"MY_VAR": "value"})

# 앱에 기본 이미지 설정
app = modal.App("my-app", image=image)

# 함수별 이미지 지정
@app.function(image=special_image)
def special():
    pass
```

---

## 함수 호출 방식

```python
@app.function()
def process(x):
    return x * 2

# 클라우드에서 실행
result = process.remote(10)

# 로컬에서 실행 (테스트용)
result = process.local(10)

# 병렬 실행
results = list(process.map([1, 2, 3, 4, 5]))

# 여러 인자 병렬 실행
results = list(process.starmap([(1, 2), (3, 4)]))
```

---

## Volume 사용

```python
# Volume 생성/참조
vol = modal.Volume.from_name("my-data", create_if_missing=True)

# 함수에 마운트
@app.function(volumes={"/data": vol})
def use_volume():
    # 파일 쓰기
    with open("/data/file.txt", "w") as f:
        f.write("data")

    # 변경사항 저장 (필수!)
    vol.commit()

    # 파일 읽기
    with open("/data/file.txt", "r") as f:
        return f.read()
```

---

## Secret 사용

```python
# 웹 대시보드에서 생성한 Secret 사용
@app.function(secrets=[modal.Secret.from_name("my-secret")])
def use_secret():
    import os
    api_key = os.environ["API_KEY"]

# 코드에서 직접 정의 (테스트용)
@app.function(secrets=[modal.Secret.from_dict({"KEY": "value"})])
def with_dict_secret():
    import os
    return os.environ["KEY"]
```

---

## 웹 엔드포인트

```python
# 간단한 엔드포인트
@app.function()
@modal.web_endpoint()
def hello():
    return {"message": "Hello!"}

# HTTP 메서드 지정
@app.function()
@modal.web_endpoint(method="POST")
def create(data: dict):
    return {"received": data}

# FastAPI 앱 배포
from fastapi import FastAPI

web_app = FastAPI()

@web_app.get("/")
def root():
    return {"status": "ok"}

@app.function()
@modal.asgi_app()
def api():
    return web_app
```

---

## 스케줄링

```python
# Period (주기)
@app.function(schedule=modal.Period(minutes=5))
@app.function(schedule=modal.Period(hours=1))
@app.function(schedule=modal.Period(days=1))

# Cron 표현식 (UTC 기준)
@app.function(schedule=modal.Cron("0 * * * *"))    # 매시간 정각
@app.function(schedule=modal.Cron("0 9 * * *"))    # 매일 09:00 UTC
@app.function(schedule=modal.Cron("0 0 * * 1"))    # 매주 월요일
@app.function(schedule=modal.Cron("*/30 * * * *")) # 30분마다
```

### 한국 시간 변환

| 한국 시간 | UTC | Cron |
|----------|-----|------|
| 09:00 | 00:00 | `0 0 * * *` |
| 12:00 | 03:00 | `0 3 * * *` |
| 18:00 | 09:00 | `0 9 * * *` |

---

## 자주 쓰는 패턴

### 모델 캐싱

```python
vol = modal.Volume.from_name("models", create_if_missing=True)

@app.function(gpu="T4", volumes={"/models": vol})
def inference(prompt):
    import os

    if os.path.exists("/models/my_model"):
        model = load("/models/my_model")
    else:
        model = download()
        save("/models/my_model", model)
        vol.commit()

    return model.predict(prompt)
```

### GPU + 웹 API

```python
@app.function(gpu="T4")
def generate(prompt):
    return model.generate(prompt)

@app.function()
@modal.web_endpoint(method="POST")
def api(data: dict):
    result = generate.remote(data["prompt"])
    return {"result": result}
```

### 병렬 배치 처리

```python
@app.function()
def process_item(item):
    return transform(item)

@app.local_entrypoint()
def main():
    items = load_data()
    results = list(process_item.map(items))
    save_results(results)
```

---

## 리소스 가이드

| 작업 | CPU | Memory | GPU |
|------|-----|--------|-----|
| 경량 작업 | 0.25 | 256MB | - |
| 일반 작업 | 1.0 | 512MB | - |
| CPU 집약적 | 2.0+ | 2GB+ | - |
| ML 추론 (소형) | 1.0 | 2GB | T4 |
| ML 추론 (중형) | 2.0 | 4GB | A10G |
| ML 학습 | 4.0 | 16GB | A100 |

---

## 디버깅

```python
# 로컬 테스트
result = my_function.local(args)

# 로깅
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.function()
def debuggable():
    logger.info("시작")
    logger.debug("상세 정보")
    logger.error("에러!")
```

```bash
# 컨테이너 쉘
modal shell app.py

# 로그 확인
modal app logs <app-name>
```

---

## 유용한 링크

- 공식 문서: https://modal.com/docs
- 예제: https://github.com/modal-labs/modal-examples
- 가격: https://modal.com/pricing
- Discord: https://discord.gg/modal

---

## References

- [Modal Documentation](https://modal.com/docs)
- [Modal API Reference](https://modal.com/docs/reference)
