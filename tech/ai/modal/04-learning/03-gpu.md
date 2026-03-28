---
date: 2026-02-02
tags:
  - tech
  - modal
  - gpu
  - ml
  - tutorial
parent: "[[../README]]"
---

# Modal - GPU 사용하기

> [[02-functions|이전: Function 정의]] | [[../README|목차]] | [[04-web-endpoints|다음: 웹 엔드포인트]]

---

## 1. GPU 기본 사용

### 가장 간단한 GPU 함수

```python
import modal

app = modal.App("gpu-example")

@app.function(gpu="T4")
def gpu_task():
    import subprocess
    result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
    return result.stdout
```

### 지원 GPU 목록

| GPU | 메모리 | 용도 | 비용 |
|-----|--------|------|------|
| T4 | 16GB | 추론, 경량 학습 | 저렴 |
| L4 | 24GB | 추론 최적화 | 중간 |
| A10G | 24GB | 추론, 중급 학습 | 중간 |
| A100-40GB | 40GB | 대규모 학습 | 높음 |
| A100-80GB | 80GB | 대규모 학습 | 높음 |
| H100 | 80GB | 최신 고성능 | 매우 높음 |
| B200 | 192GB | 초대형 모델 | 최고 |

### GPU 지정 방법

```python
# 문자열로 지정
@app.function(gpu="T4")
@app.function(gpu="A10G")
@app.function(gpu="A100")
@app.function(gpu="H100")

# GPU 개수 지정
@app.function(gpu="A100:2")  # A100 2개

# modal.gpu 객체 사용
@app.function(gpu=modal.gpu.T4())
@app.function(gpu=modal.gpu.A100(count=2))
```

---

## 2. PyTorch와 GPU

### PyTorch 이미지 설정

```python
import modal

# CUDA가 포함된 PyTorch 이미지
pytorch_image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "torch",
    "torchvision",
    "torchaudio",
)

app = modal.App("pytorch-example", image=pytorch_image)

@app.function(gpu="T4")
def check_pytorch_gpu():
    import torch

    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Device count: {torch.cuda.device_count()}")
    print(f"Device name: {torch.cuda.get_device_name(0)}")

    # GPU 연산 테스트
    x = torch.randn(1000, 1000, device="cuda")
    y = torch.randn(1000, 1000, device="cuda")
    z = torch.matmul(x, y)

    return f"결과 shape: {z.shape}"

@app.local_entrypoint()
def main():
    print(check_pytorch_gpu.remote())
```

---

## 3. HuggingFace 모델 서빙

### 텍스트 생성 모델

```python
import modal

app = modal.App("huggingface-llm")

image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "torch",
    "transformers",
    "accelerate",
)

@app.function(gpu="T4", image=image, timeout=600)
def generate_text(prompt: str, max_length: int = 100):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    model_name = "gpt2"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        do_sample=True,
        temperature=0.7
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

@app.local_entrypoint()
def main():
    result = generate_text.remote("The future of AI is")
    print(result)
```

---

## 4. 모델 캐싱 (Volume)

모델을 매번 다운로드하면 시간이 오래 걸립니다. Volume을 사용해 캐싱하세요.

```python
import modal

app = modal.App("cached-model")

# 모델 저장용 Volume
model_volume = modal.Volume.from_name("model-cache", create_if_missing=True)

image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "torch", "transformers", "accelerate"
)

MODEL_DIR = "/model_cache"

@app.function(
    gpu="T4",
    image=image,
    volumes={MODEL_DIR: model_volume},
    timeout=600
)
def generate_with_cache(prompt: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    import os

    model_name = "gpt2"
    cache_path = f"{MODEL_DIR}/{model_name}"

    # 캐시에서 로드 또는 다운로드
    if os.path.exists(cache_path):
        print("캐시에서 모델 로드")
        model = AutoModelForCausalLM.from_pretrained(cache_path)
        tokenizer = AutoTokenizer.from_pretrained(cache_path)
    else:
        print("모델 다운로드 중...")
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # 캐시에 저장
        model.save_pretrained(cache_path)
        tokenizer.save_pretrained(cache_path)
        model_volume.commit()  # 변경사항 저장

    model = model.to("cuda")
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_length=50)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

---

## 5. 이미지 생성 (Stable Diffusion)

```python
import modal

app = modal.App("stable-diffusion")

image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "torch",
    "diffusers",
    "transformers",
    "accelerate",
)

model_volume = modal.Volume.from_name("sd-models", create_if_missing=True)

@app.function(
    gpu="A10G",
    image=image,
    volumes={"/models": model_volume},
    timeout=600
)
def generate_image(prompt: str) -> bytes:
    from diffusers import DiffusionPipeline
    import torch
    import io

    pipe = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        cache_dir="/models"
    )
    pipe.to("cuda")

    image = pipe(prompt, num_inference_steps=30).images[0]

    # 바이트로 변환
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()

@app.local_entrypoint()
def main():
    image_bytes = generate_image.remote("a cat astronaut in space")

    with open("output.png", "wb") as f:
        f.write(image_bytes)
    print("이미지 저장됨: output.png")
```

---

## 6. GPU 최적화 팁

### 메모리 관리

```python
@app.function(gpu="T4")
def optimized_inference():
    import torch
    import gc

    # 추론 시 그래디언트 비활성화
    with torch.no_grad():
        # ... 추론 코드

    # 메모리 정리
    torch.cuda.empty_cache()
    gc.collect()
```

### 배치 처리

```python
@app.function(gpu="T4")
def batch_inference(inputs: list) -> list:
    # 여러 입력을 한 번에 처리
    model = load_model()
    results = model(inputs)  # 배치 추론
    return results
```

### GPU 메모리 확인

```python
@app.function(gpu="T4")
def check_memory():
    import torch

    total = torch.cuda.get_device_properties(0).total_memory
    reserved = torch.cuda.memory_reserved(0)
    allocated = torch.cuda.memory_allocated(0)
    free = reserved - allocated

    return {
        "total_gb": total / 1e9,
        "reserved_gb": reserved / 1e9,
        "allocated_gb": allocated / 1e9,
        "free_gb": free / 1e9
    }
```

---

## 7. GPU 선택 가이드

```
어떤 작업인가?
├── 추론 (Inference)
│   ├── 소형 모델 (GPT-2, DistilBERT) → T4
│   ├── 중형 모델 (Llama-7B) → A10G
│   ├── 대형 모델 (Llama-70B) → A100/H100
│   └── 이미지 생성 (SD, SDXL) → A10G
│
├── 학습 (Training)
│   ├── 소규모 파인튜닝 → T4/A10G
│   ├── 중규모 학습 → A100-40GB
│   └── 대규모 학습 → A100-80GB/H100
│
└── 비용 최적화
    ├── 프로토타입 → T4 (가장 저렴)
    ├── 프로덕션 추론 → L4 (효율적)
    └── 고성능 필요 → H100
```

---

## 8. 체크리스트

### 학습 확인

- [ ] GPU 함수 작성 가능
- [ ] 다양한 GPU 타입 이해
- [ ] PyTorch GPU 사용 가능
- [ ] HuggingFace 모델 서빙 가능
- [ ] Volume을 이용한 모델 캐싱 이해
- [ ] GPU 메모리 관리 팁 이해

---

## 다음 단계

> [!tip] 다음으로
> GPU 사용법을 익혔다면 [[04-web-endpoints|웹 엔드포인트 만들기]]로 넘어가세요.

---

## References

- [Modal GPU Guide](https://modal.com/docs/guide/gpu)
- [Modal GPU Pricing](https://modal.com/pricing)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
