---
date: 2026-02-02
tags:
  - tech
  - modal
  - volumes
  - storage
  - tutorial
parent: "[[../README]]"
---

# Modal - 볼륨과 영구 저장소

> [[04-web-endpoints|이전: 웹 엔드포인트]] | [[../README|목차]] | [[06-scheduling|다음: 스케줄링]]

---

## 1. Volume 개요

### Volume이란?

Modal Volume은 함수 실행 간에 데이터를 유지하는 영구 저장소입니다.

사용 사례:
- ML 모델 가중치 캐싱
- 데이터셋 저장
- 생성된 파일 저장
- 로그 저장

### Volume vs 일반 파일

| 특성 | Volume | 컨테이너 파일 |
|------|--------|--------------|
| 영구성 | O (유지됨) | X (컨테이너 종료 시 삭제) |
| 공유 | 여러 함수 간 공유 | 해당 컨테이너만 |
| 속도 | 네트워크 I/O | 로컬 I/O |
| 용도 | 모델, 데이터셋 | 임시 파일 |

---

## 2. Volume 기본 사용

### Volume 생성

```python
import modal

app = modal.App("volume-example")

# Volume 생성 (없으면 새로 생성)
my_volume = modal.Volume.from_name("my-data", create_if_missing=True)
```

### 함수에 마운트

```python
MOUNT_PATH = "/data"

@app.function(volumes={MOUNT_PATH: my_volume})
def write_data():
    # /data 경로로 Volume에 접근
    with open(f"{MOUNT_PATH}/hello.txt", "w") as f:
        f.write("Hello, Volume!")

    # 변경사항 저장 (중요!)
    my_volume.commit()
    return "저장 완료"

@app.function(volumes={MOUNT_PATH: my_volume})
def read_data():
    # 다른 함수에서 읽기
    with open(f"{MOUNT_PATH}/hello.txt", "r") as f:
        return f.read()
```

### commit() 중요성

```python
@app.function(volumes={"/data": my_volume})
def save_file():
    with open("/data/file.txt", "w") as f:
        f.write("data")

    # commit() 없으면 변경사항 유실!
    my_volume.commit()
```

---

## 3. 모델 캐싱

### HuggingFace 모델 캐싱

```python
import modal

app = modal.App("model-cache")

# 모델 캐시용 Volume
model_volume = modal.Volume.from_name("hf-models", create_if_missing=True)

image = modal.Image.debian_slim().pip_install(
    "torch", "transformers"
)

MODEL_CACHE = "/models"

@app.function(
    gpu="T4",
    image=image,
    volumes={MODEL_CACHE: model_volume}
)
def load_model():
    from transformers import AutoModel, AutoTokenizer
    import os

    model_name = "bert-base-uncased"
    cache_dir = f"{MODEL_CACHE}/{model_name}"

    # 캐시 확인
    if os.path.exists(cache_dir):
        print("캐시에서 로드")
    else:
        print("다운로드 후 캐시 저장")

    model = AutoModel.from_pretrained(
        model_name,
        cache_dir=cache_dir
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=cache_dir
    )

    # 새로 다운로드했다면 commit
    model_volume.commit()

    return "모델 로드 완료"
```

### 다운로드 전용 함수

```python
@app.function(
    image=image,
    volumes={MODEL_CACHE: model_volume}
)
def download_model(model_name: str):
    """사전에 모델 다운로드"""
    from transformers import AutoModel, AutoTokenizer

    cache_dir = f"{MODEL_CACHE}/{model_name}"

    AutoModel.from_pretrained(model_name, cache_dir=cache_dir)
    AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)

    model_volume.commit()
    return f"{model_name} 다운로드 완료"
```

---

## 4. 데이터 파이프라인

### 파일 업로드 및 처리

```python
import modal

app = modal.App("data-pipeline")

data_volume = modal.Volume.from_name("pipeline-data", create_if_missing=True)

DATA_PATH = "/data"

@app.function(volumes={DATA_PATH: data_volume})
def upload_data(filename: str, content: bytes):
    """데이터 업로드"""
    with open(f"{DATA_PATH}/raw/{filename}", "wb") as f:
        f.write(content)
    data_volume.commit()
    return f"{filename} 업로드 완료"

@app.function(volumes={DATA_PATH: data_volume})
def process_data(filename: str):
    """데이터 처리"""
    import json

    # 원본 읽기
    with open(f"{DATA_PATH}/raw/{filename}", "r") as f:
        data = json.load(f)

    # 처리
    processed = transform(data)

    # 결과 저장
    with open(f"{DATA_PATH}/processed/{filename}", "w") as f:
        json.dump(processed, f)

    data_volume.commit()
    return f"{filename} 처리 완료"

@app.function(volumes={DATA_PATH: data_volume})
def list_files():
    """저장된 파일 목록"""
    import os
    files = os.listdir(f"{DATA_PATH}/raw")
    return files
```

---

## 5. Volume 관리

### CLI 명령어

```bash
# Volume 목록
modal volume list

# Volume 내용 확인
modal volume ls <volume-name>

# 파일 다운로드
modal volume get <volume-name> /path/to/file ./local/path

# 파일 업로드
modal volume put <volume-name> ./local/file /remote/path

# Volume 삭제
modal volume delete <volume-name>
```

### 코드에서 관리

```python
@app.function(volumes={"/data": my_volume})
def manage_volume():
    import os
    import shutil

    # 파일 목록
    files = os.listdir("/data")

    # 파일 삭제
    os.remove("/data/old_file.txt")

    # 디렉토리 삭제
    shutil.rmtree("/data/old_dir")

    my_volume.commit()
```

---

## 6. 여러 Volume 사용

```python
import modal

app = modal.App("multi-volume")

model_volume = modal.Volume.from_name("models", create_if_missing=True)
data_volume = modal.Volume.from_name("datasets", create_if_missing=True)
output_volume = modal.Volume.from_name("outputs", create_if_missing=True)

@app.function(
    volumes={
        "/models": model_volume,
        "/data": data_volume,
        "/output": output_volume
    }
)
def train():
    # 모델 로드
    model = load_from("/models/checkpoint.pt")

    # 데이터 로드
    data = load_from("/data/train.csv")

    # 학습
    trained_model = train_model(model, data)

    # 결과 저장
    save_to("/output/final_model.pt", trained_model)

    output_volume.commit()
```

---

## 7. 주의사항

### Volume 사용 시 주의

1. **commit() 필수**: 변경 후 반드시 `commit()` 호출
2. **동시 쓰기 주의**: 여러 함수가 동시에 같은 파일 쓰기 피하기
3. **용량 관리**: 불필요한 파일 정기적으로 정리
4. **네트워크 지연**: 대용량 파일은 읽기/쓰기 시간 고려

### 안티패턴

```python
# 나쁜 예: commit 누락
@app.function(volumes={"/data": vol})
def bad_write():
    with open("/data/file.txt", "w") as f:
        f.write("data")
    # commit() 없음 -> 변경사항 유실!

# 좋은 예
@app.function(volumes={"/data": vol})
def good_write():
    with open("/data/file.txt", "w") as f:
        f.write("data")
    vol.commit()  # 변경사항 저장
```

### 성능 최적화

```python
# 대량 파일 처리 시 배치로 commit
@app.function(volumes={"/data": vol})
def batch_write(items: list):
    for item in items:
        save_file(item)

    # 모든 작업 후 한 번만 commit
    vol.commit()
```

---

## 8. 실전 예제: 이미지 처리 파이프라인

```python
import modal

app = modal.App("image-pipeline")

images_volume = modal.Volume.from_name("images", create_if_missing=True)

image = modal.Image.debian_slim().pip_install("pillow")

@app.function(image=image, volumes={"/images": images_volume})
def upload_image(filename: str, data: bytes):
    with open(f"/images/raw/{filename}", "wb") as f:
        f.write(data)
    images_volume.commit()

@app.function(image=image, volumes={"/images": images_volume})
def resize_image(filename: str, size: tuple):
    from PIL import Image
    import io

    # 원본 로드
    with open(f"/images/raw/{filename}", "rb") as f:
        img = Image.open(io.BytesIO(f.read()))

    # 리사이즈
    resized = img.resize(size)

    # 저장
    output_path = f"/images/resized/{size[0]}x{size[1]}_{filename}"
    resized.save(output_path)

    images_volume.commit()
    return output_path

@app.function(image=image, volumes={"/images": images_volume})
def get_image(path: str) -> bytes:
    with open(f"/images/{path}", "rb") as f:
        return f.read()
```

---

## 9. 체크리스트

### 학습 확인

- [ ] Volume 생성 및 마운트 가능
- [ ] commit()의 중요성 이해
- [ ] 모델 캐싱에 Volume 활용 가능
- [ ] CLI로 Volume 관리 가능
- [ ] 여러 Volume 동시 사용 가능
- [ ] Volume 사용 시 주의사항 숙지

---

## 다음 단계

> [!tip] 다음으로
> Volume 사용법을 익혔다면 [[06-scheduling|스케줄링과 Cron]]을 배워보세요.

---

## References

- [Modal Volumes Guide](https://modal.com/docs/guide/volumes)
- [Modal Volume CLI](https://modal.com/docs/reference/cli/volume)
