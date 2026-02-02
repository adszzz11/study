---
date: 2026-02-02
tags:
  - tech
  - modal
  - projects
  - best-practices
parent: "[[README]]"
---

# Modal - 실전 프로젝트와 Best Practices

> [[04-learning/06-scheduling|이전: 스케줄링]] | [[README|목차]] | [[cheatsheet|다음: 치트시트]]

---

## 1. 프로젝트 구조

### 권장 프로젝트 구조

```
my-modal-project/
├── app/
│   ├── __init__.py
│   ├── main.py          # 메인 앱 정의
│   ├── functions.py     # 함수 모듈
│   ├── models.py        # Pydantic 모델
│   └── utils.py         # 유틸리티
├── tests/
│   └── test_functions.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### 모듈화된 앱 구조

```python
# app/main.py
import modal
from app.functions import process_data, generate_text
from app.config import app, image

# 함수들을 앱에 등록
app.function()(process_data)
app.function(gpu="T4", image=image)(generate_text)
```

```python
# app/config.py
import modal

app = modal.App("my-project")

image = modal.Image.debian_slim().pip_install(
    "torch", "transformers"
)

model_volume = modal.Volume.from_name("models", create_if_missing=True)
```

---

## 2. Best Practices

### DO (권장)

```python
# 1. 모델 캐싱 사용
model_volume = modal.Volume.from_name("models", create_if_missing=True)

@app.function(volumes={"/models": model_volume})
def load_model():
    # 캐시된 모델 사용
    pass

# 2. 타입 힌트 사용
@app.function()
def process(data: list[str]) -> dict:
    return {"count": len(data)}

# 3. 에러 처리
@app.function(retries=3)
def reliable_task():
    try:
        return do_work()
    except Exception as e:
        logger.error(f"Error: {e}")
        raise

# 4. 환경 변수는 Secret 사용
@app.function(secrets=[modal.Secret.from_name("api-keys")])
def secure_function():
    import os
    api_key = os.environ["API_KEY"]

# 5. 적절한 리소스 설정
@app.function(cpu=2, memory=2048, timeout=600)
def resource_intensive():
    pass

# 6. 로깅 활용
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.function()
def logged_task():
    logger.info("작업 시작")
    # ...
    logger.info("작업 완료")
```

### DON'T (피해야 할 것)

```python
# 1. 하드코딩된 시크릿
@app.function()
def bad_secret():
    api_key = "sk-xxxxx"  # 절대 금지!

# 2. commit() 누락
@app.function(volumes={"/data": vol})
def bad_volume():
    save_file("/data/file.txt")
    # vol.commit() 빠뜨림 - 데이터 유실!

# 3. 과도한 리소스 요청
@app.function(gpu="A100", cpu=8, memory=32000)
def simple_task():
    return 1 + 1  # 리소스 낭비

# 4. 무한 루프/긴 타임아웃
@app.function(timeout=86400)  # 24시간 타임아웃은 비효율적
def long_running():
    while True:
        pass

# 5. 로컬 파일 경로 사용
@app.function()
def bad_path():
    open("/Users/me/file.txt")  # 클라우드에는 없음!
```

---

## 3. 실전 프로젝트 예제

### 프로젝트 1: LLM 챗봇 API

```python
import modal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = modal.App("llm-chatbot")

image = modal.Image.debian_slim().pip_install(
    "torch", "transformers", "accelerate", "fastapi"
)

model_volume = modal.Volume.from_name("llm-models", create_if_missing=True)

MODEL_PATH = "/models"
MODEL_NAME = "microsoft/DialoGPT-medium"

# 모델 다운로드 (한 번만 실행)
@app.function(image=image, volumes={MODEL_PATH: model_volume})
def download_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model.save_pretrained(f"{MODEL_PATH}/dialogpt")
    tokenizer.save_pretrained(f"{MODEL_PATH}/dialogpt")
    model_volume.commit()

    return "모델 다운로드 완료"

# 추론 함수
@app.function(
    gpu="T4",
    image=image,
    volumes={MODEL_PATH: model_volume}
)
def generate_response(message: str, history: list = None) -> str:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    tokenizer = AutoTokenizer.from_pretrained(f"{MODEL_PATH}/dialogpt")
    model = AutoModelForCausalLM.from_pretrained(f"{MODEL_PATH}/dialogpt").to("cuda")

    # 대화 히스토리 구성
    if history:
        context = " ".join(history[-5:])  # 최근 5개 메시지
        input_text = f"{context} {message}"
    else:
        input_text = message

    inputs = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt").to("cuda")

    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7
        )

    response = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return response

# API 엔드포인트
web_app = FastAPI(title="LLM Chatbot API")

class ChatRequest(BaseModel):
    message: str
    history: list[str] = []

class ChatResponse(BaseModel):
    response: str

@web_app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = generate_response.remote(request.message, request.history)
    return ChatResponse(response=response)

@web_app.get("/health")
def health():
    return {"status": "healthy"}

@app.function(image=image)
@modal.asgi_app()
def api():
    return web_app
```

### 프로젝트 2: 이미지 처리 파이프라인

```python
import modal
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response

app = modal.App("image-pipeline")

image = modal.Image.debian_slim().pip_install(
    "pillow", "numpy", "fastapi", "python-multipart"
)

storage = modal.Volume.from_name("image-storage", create_if_missing=True)

# 이미지 처리 함수들
@app.function(image=image)
def resize_image(img_bytes: bytes, width: int, height: int) -> bytes:
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(img_bytes))
    resized = img.resize((width, height), Image.Resampling.LANCZOS)

    output = io.BytesIO()
    resized.save(output, format="PNG")
    return output.getvalue()

@app.function(image=image)
def apply_filter(img_bytes: bytes, filter_type: str) -> bytes:
    from PIL import Image, ImageFilter
    import io

    img = Image.open(io.BytesIO(img_bytes))

    filters = {
        "blur": ImageFilter.BLUR,
        "sharpen": ImageFilter.SHARPEN,
        "contour": ImageFilter.CONTOUR,
        "edge": ImageFilter.FIND_EDGES,
    }

    if filter_type in filters:
        img = img.filter(filters[filter_type])

    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()

@app.function(image=image)
def batch_process(images: list[bytes], operation: str, **kwargs) -> list[bytes]:
    """여러 이미지 병렬 처리"""
    if operation == "resize":
        return list(resize_image.map(images, kwargs.get("width", 256), kwargs.get("height", 256)))
    elif operation == "filter":
        return list(apply_filter.map(images, kwargs.get("filter_type", "blur")))
    return images

# API
web_app = FastAPI(title="Image Processing API")

@web_app.post("/resize")
async def api_resize(
    file: UploadFile = File(...),
    width: int = 256,
    height: int = 256
):
    contents = await file.read()
    result = resize_image.remote(contents, width, height)
    return Response(content=result, media_type="image/png")

@web_app.post("/filter/{filter_type}")
async def api_filter(filter_type: str, file: UploadFile = File(...)):
    contents = await file.read()
    result = apply_filter.remote(contents, filter_type)
    return Response(content=result, media_type="image/png")

@app.function(image=image)
@modal.asgi_app()
def api():
    return web_app
```

### 프로젝트 3: 데이터 수집 및 분석 봇

```python
import modal
from datetime import datetime

app = modal.App("data-bot")

image = modal.Image.debian_slim().pip_install(
    "requests", "pandas", "beautifulsoup4"
)

data_volume = modal.Volume.from_name("collected-data", create_if_missing=True)

DATA_PATH = "/data"

# 데이터 수집 (1시간마다)
@app.function(
    image=image,
    schedule=modal.Period(hours=1),
    volumes={DATA_PATH: data_volume}
)
def collect_data():
    import requests
    import json

    # 데이터 소스에서 수집
    sources = [
        "https://api.example.com/data1",
        "https://api.example.com/data2",
    ]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    collected = []

    for url in sources:
        try:
            response = requests.get(url, timeout=30)
            collected.append(response.json())
        except Exception as e:
            print(f"수집 실패: {url} - {e}")

    # 저장
    with open(f"{DATA_PATH}/raw/{timestamp}.json", "w") as f:
        json.dump(collected, f)

    data_volume.commit()
    print(f"데이터 수집 완료: {timestamp}")

# 일일 분석 (매일 오전 9시 한국시간 = UTC 00:00)
@app.function(
    image=image,
    schedule=modal.Cron("0 0 * * *"),
    volumes={DATA_PATH: data_volume},
    secrets=[modal.Secret.from_name("slack-webhook")]
)
def daily_analysis():
    import pandas as pd
    import json
    import os
    from datetime import datetime, timedelta

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    # 어제 데이터 로드
    raw_files = [f for f in os.listdir(f"{DATA_PATH}/raw") if f.startswith(yesterday)]

    all_data = []
    for file in raw_files:
        with open(f"{DATA_PATH}/raw/{file}") as f:
            all_data.extend(json.load(f))

    if not all_data:
        return "데이터 없음"

    # 분석
    df = pd.DataFrame(all_data)
    summary = {
        "total_records": len(df),
        "unique_items": df["item_id"].nunique() if "item_id" in df else 0,
        "date": yesterday
    }

    # 리포트 저장
    with open(f"{DATA_PATH}/reports/{yesterday}_summary.json", "w") as f:
        json.dump(summary, f)

    data_volume.commit()

    # Slack 알림
    notify_slack(f"일일 분석 완료: {summary}")

    return summary

def notify_slack(message):
    import requests
    import os
    webhook = os.environ.get("SLACK_WEBHOOK")
    if webhook:
        requests.post(webhook, json={"text": message})

# 수동 분석 트리거
@app.local_entrypoint()
def main():
    collect_data.remote()
    print("데이터 수집 완료")
```

---

## 4. 디버깅 팁

### 로컬 테스트

```python
@app.function()
def my_function(x):
    return x * 2

# 로컬에서 테스트
result = my_function.local(10)
print(result)  # 20
```

### 컨테이너 쉘 접속

```bash
# 컨테이너 환경에서 직접 디버깅
modal shell app.py
```

### 로그 확인

```bash
# 실시간 로그
modal app logs <app-name>

# 특정 함수 로그
modal app logs <app-name> --filter <function-name>
```

### print vs logging

```python
import logging

# 프로덕션에서는 logging 사용
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.function()
def production_code():
    logger.info("작업 시작")
    logger.debug("디버그 정보")
    logger.error("에러 발생")
```

---

## 5. 성능 최적화

### 병렬 처리 활용

```python
# 순차 처리 (느림)
results = []
for item in items:
    results.append(process.remote(item))

# 병렬 처리 (빠름)
results = list(process.map(items))
```

### 캐싱 전략

```python
# 모델/데이터 캐싱
model_volume = modal.Volume.from_name("cache", create_if_missing=True)

@app.function(volumes={"/cache": model_volume})
def with_cache():
    if os.path.exists("/cache/model.pt"):
        model = load_from_cache()
    else:
        model = download_model()
        save_to_cache(model)
        model_volume.commit()
```

### 적절한 리소스 설정

```python
# 작업에 맞는 리소스 선택
@app.function(cpu=0.25)          # 경량 작업
def light_task(): pass

@app.function(cpu=2, memory=4096)  # CPU 집약적
def cpu_intensive(): pass

@app.function(gpu="T4")           # GPU 추론
def gpu_inference(): pass

@app.function(gpu="A100")         # 대규모 학습
def gpu_training(): pass
```

---

## 6. 체크리스트

### 프로젝트 시작 전

- [ ] 요구사항 정리 (CPU/GPU, 메모리, 타임아웃)
- [ ] 프로젝트 구조 설계
- [ ] Secret 준비 (API 키 등)
- [ ] Volume 계획 (캐싱, 저장)

### 개발 중

- [ ] 로컬 테스트 (`.local()`)
- [ ] 타입 힌트 추가
- [ ] 에러 처리 구현
- [ ] 로깅 추가

### 배포 전

- [ ] 리소스 설정 최적화
- [ ] 시크릿 확인
- [ ] 타임아웃 적절한지 확인
- [ ] Volume commit 확인

---

## 다음 단계

> [!tip] 다음으로
> 실전 프로젝트를 경험했다면 [[cheatsheet|치트시트]]로 빠른 참조를 준비하세요.

---

## References

- [Modal Examples Repository](https://github.com/modal-labs/modal-examples)
- [Modal Best Practices](https://modal.com/docs/guide/best-practices)
- [Modal Blog](https://modal.com/blog)
