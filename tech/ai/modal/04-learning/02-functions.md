---
date: 2026-02-02
tags:
  - tech
  - modal
  - functions
  - tutorial
parent: "[[../README]]"
---

# Modal - Function 정의와 데코레이터

> [[01-setup|이전: 설치]] | [[../README|목차]] | [[03-gpu|다음: GPU 사용]]

---

## 1. Function 기본 개념

### Modal Function이란?

Modal Function은 클라우드에서 실행되는 Python 함수입니다.

```python
import modal

app = modal.App("my-app")

# 이 함수는 클라우드 컨테이너에서 실행됨
@app.function()
def my_function(x):
    return x * 2
```

### 호출 방식

| 호출 방식 | 설명 | 사용 |
|----------|------|------|
| `.remote()` | 클라우드에서 실행 | `my_function.remote(10)` |
| `.local()` | 로컬에서 실행 | `my_function.local(10)` |
| `.map()` | 병렬 실행 | `my_function.map([1, 2, 3])` |

```python
# 클라우드에서 실행
result = my_function.remote(10)  # 20

# 로컬에서 실행 (테스트용)
result = my_function.local(10)  # 20

# 여러 입력 병렬 처리
results = list(my_function.map([1, 2, 3, 4, 5]))
# [2, 4, 6, 8, 10]
```

---

## 2. @app.function() 데코레이터

### 기본 옵션

```python
@app.function(
    cpu=1.0,           # CPU 코어 수 (기본 0.125)
    memory=512,        # 메모리 MB (기본 128)
    timeout=3600,      # 타임아웃 초 (기본 300)
    retries=3,         # 재시도 횟수
)
def compute_task():
    pass
```

### 주요 옵션 정리

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `cpu` | CPU 코어 수 | 0.125 |
| `memory` | 메모리 (MB) | 128 |
| `timeout` | 실행 제한 시간 (초) | 300 |
| `retries` | 실패 시 재시도 횟수 | 0 |
| `gpu` | GPU 종류 | None |
| `image` | 커스텀 이미지 | 기본 이미지 |
| `secrets` | Secret 목록 | [] |
| `volumes` | Volume 마운트 | {} |
| `concurrency_limit` | 동시 실행 제한 | None |

---

## 3. Image (컨테이너 환경)

### 기본 이미지

```python
import modal

# Debian 기반 이미지
image = modal.Image.debian_slim()

# Python 패키지 추가
image = modal.Image.debian_slim().pip_install(
    "pandas",
    "numpy",
    "scikit-learn"
)

app = modal.App("my-app", image=image)

@app.function()
def process_data():
    import pandas as pd  # 이제 사용 가능
    return pd.DataFrame()
```

### 함수별 이미지 지정

```python
# 기본 이미지
default_image = modal.Image.debian_slim()

# ML 전용 이미지
ml_image = modal.Image.debian_slim().pip_install(
    "torch",
    "transformers"
)

app = modal.App("my-app", image=default_image)

@app.function()
def simple_task():
    pass  # 기본 이미지 사용

@app.function(image=ml_image)
def ml_task():
    import torch  # ml_image에서 사용 가능
    pass
```

### 이미지 빌드 옵션

```python
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("package1", "package2")
    .apt_install("ffmpeg", "libsm6")  # 시스템 패키지
    .run_commands("echo 'setup complete'")  # 쉘 명령
    .env({"MY_VAR": "value"})  # 환경 변수
)
```

---

## 4. 병렬 처리 (map)

### 기본 map 사용

```python
@app.function()
def process_item(item):
    return item * 2

@app.local_entrypoint()
def main():
    items = [1, 2, 3, 4, 5]

    # 5개 컨테이너에서 병렬 실행
    results = list(process_item.map(items))
    print(results)  # [2, 4, 6, 8, 10]
```

### starmap (여러 인자)

```python
@app.function()
def add(a, b):
    return a + b

@app.local_entrypoint()
def main():
    pairs = [(1, 2), (3, 4), (5, 6)]

    # 여러 인자 전달
    results = list(add.starmap(pairs))
    print(results)  # [3, 7, 11]
```

### 동시성 제어

```python
# 최대 10개 컨테이너만 동시 실행
@app.function(concurrency_limit=10)
def limited_task(x):
    return x
```

---

## 5. Secret 관리

### Secret 생성 (웹 대시보드)

1. [modal.com/secrets](https://modal.com/secrets) 접속
2. "Create new secret" 클릭
3. 이름과 키-값 쌍 입력

### Secret 사용

```python
import modal
import os

app = modal.App("secret-example")

@app.function(secrets=[modal.Secret.from_name("my-api-key")])
def use_secret():
    # 환경 변수로 접근
    api_key = os.environ["API_KEY"]
    return f"Key: {api_key[:4]}..."
```

### 환경 변수 직접 전달

```python
@app.function(
    secrets=[
        modal.Secret.from_dict({"MY_VAR": "value"})
    ]
)
def with_env():
    import os
    return os.environ["MY_VAR"]
```

---

## 6. 진입점 (Entrypoint)

### @app.local_entrypoint()

```python
@app.local_entrypoint()
def main():
    """modal run 시 실행되는 함수"""
    result = my_function.remote("input")
    print(result)
```

로컬에서 실행되며 클라우드 함수를 호출하는 오케스트레이션 역할

### 인자 받기

```python
@app.local_entrypoint()
def main(name: str = "World", count: int = 1):
    for _ in range(count):
        print(hello.remote(name))
```

실행:
```bash
modal run app.py --name "Modal" --count 3
```

---

## 7. 실전 예제

### 파일 처리 파이프라인

```python
import modal

app = modal.App("file-processor")

image = modal.Image.debian_slim().pip_install("pillow")

@app.function(image=image)
def resize_image(image_data: bytes, size: tuple) -> bytes:
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(image_data))
    img = img.resize(size)

    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()

@app.function(image=image)
def process_batch(image_list: list) -> list:
    results = []
    for img_data in image_list:
        resized = resize_image.remote(img_data, (256, 256))
        results.append(resized)
    return results

@app.local_entrypoint()
def main():
    # 예시: 여러 이미지 병렬 처리
    with open("test.png", "rb") as f:
        img_data = f.read()

    results = list(resize_image.map([img_data] * 10))
    print(f"처리된 이미지: {len(results)}개")
```

---

## 8. 체크리스트

### 학습 확인

- [ ] @app.function() 데코레이터 이해
- [ ] .remote() vs .local() 차이 이해
- [ ] Image 커스터마이징 가능
- [ ] map()으로 병렬 처리 가능
- [ ] Secret 사용 방법 이해
- [ ] @app.local_entrypoint() 이해

---

## 다음 단계

> [!tip] 다음으로
> Function의 기본을 익혔다면 [[03-gpu|GPU 사용하기]]로 넘어가세요.

---

## References

- [Modal Functions Guide](https://modal.com/docs/guide/functions)
- [Modal Image Guide](https://modal.com/docs/guide/custom-container)
- [Modal Secrets Guide](https://modal.com/docs/guide/secrets)
