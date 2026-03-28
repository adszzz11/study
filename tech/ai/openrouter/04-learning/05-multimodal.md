# OpenRouter 멀티모달

> 이미지, PDF 분석하기

## 멀티모달이란?

텍스트뿐만 아니라 **이미지, PDF 등 다양한 형식의 입력**을 처리하는 기능입니다.

```
지원 형식:
- 이미지: PNG, JPEG, GIF, WebP
- 문서: PDF (일부 모델)
- 텍스트: 기본 지원
```

---

## 지원 모델

### 멀티모달 지원 모델

| 모델 | 이미지 | PDF | 특징 |
|-----|-------|-----|------|
| `anthropic/claude-sonnet-4` | O | O | 가장 안정적 |
| `openai/gpt-4o` | O | X | 이미지 분석 강점 |
| `google/gemini-2.0-flash` | O | O | 긴 문서 처리 |
| `anthropic/claude-3-haiku` | O | X | 빠르고 저렴 |

---

## 이미지 분석

### 1. URL로 이미지 전달

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."
)

response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 이미지를 설명해주세요."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
```

### 2. Base64로 이미지 전달

```python
import base64

def encode_image(image_path: str) -> str:
    """이미지 파일을 base64로 인코딩"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 로컬 이미지 분석
image_base64 = encode_image("./my_image.png")

response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 이미지에서 텍스트를 추출해주세요."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
```

### 3. 여러 이미지 동시 분석

```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "두 이미지를 비교해주세요."},
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/image1.jpg"}
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/image2.jpg"}
                }
            ]
        }
    ]
)
```

---

## PDF 분석

### 1. PDF URL로 전달

```python
# Claude 모델에서 PDF 지원
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 PDF 문서를 요약해주세요."},
                {
                    "type": "file",
                    "file": {
                        "url": "https://example.com/document.pdf"
                    }
                }
            ]
        }
    ]
)
```

### 2. Base64로 PDF 전달

```python
def encode_pdf(pdf_path: str) -> str:
    """PDF 파일을 base64로 인코딩"""
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode("utf-8")

pdf_base64 = encode_pdf("./document.pdf")

response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 PDF의 주요 내용을 정리해주세요."},
                {
                    "type": "file",
                    "file": {
                        "url": f"data:application/pdf;base64,{pdf_base64}"
                    }
                }
            ]
        }
    ]
)
```

---

## 실용적인 예제

### 1. 이미지 OCR (텍스트 추출)

```python
def extract_text_from_image(image_path: str) -> str:
    """이미지에서 텍스트 추출"""
    image_base64 = encode_image(image_path)

    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "이 이미지에서 모든 텍스트를 정확히 추출해주세요. 원본 형식을 유지해주세요."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

# 사용
text = extract_text_from_image("./receipt.png")
print(text)
```

### 2. 영수증 분석

```python
def analyze_receipt(image_path: str) -> dict:
    """영수증 이미지 분석하여 구조화된 데이터 반환"""
    image_base64 = encode_image(image_path)

    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """이 영수증을 분석하여 다음 JSON 형식으로 반환해주세요:
{
    "store_name": "가게 이름",
    "date": "날짜",
    "items": [{"name": "품목", "price": 가격}],
    "total": 총액
}"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        response_format={"type": "json_object"}
    )

    import json
    return json.loads(response.choices[0].message.content)

# 사용
receipt_data = analyze_receipt("./receipt.jpg")
print(f"총액: {receipt_data['total']}원")
```

### 3. 다이어그램 설명

```python
def explain_diagram(image_url: str) -> str:
    """다이어그램/차트 설명"""
    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "이 다이어그램/차트를 자세히 설명해주세요. 주요 구성 요소와 관계를 설명해주세요."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content
```

### 4. PDF 문서 요약

```python
def summarize_pdf(pdf_path: str, max_pages: int = None) -> str:
    """PDF 문서 요약"""
    pdf_base64 = encode_pdf(pdf_path)

    prompt = "이 PDF 문서의 주요 내용을 요약해주세요."
    if max_pages:
        prompt += f" 처음 {max_pages}페이지를 중심으로 분석해주세요."

    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "file",
                        "file": {
                            "url": f"data:application/pdf;base64,{pdf_base64}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content
```

### 5. 이미지 비교

```python
def compare_images(image_path1: str, image_path2: str) -> str:
    """두 이미지 비교 분석"""
    img1_base64 = encode_image(image_path1)
    img2_base64 = encode_image(image_path2)

    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "두 이미지를 비교하여 차이점과 공통점을 설명해주세요."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img1_base64}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img2_base64}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content
```

---

## JavaScript 예제

### 이미지 분석

```javascript
import OpenAI from 'openai';
import fs from 'fs';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
});

// URL로 이미지 분석
async function analyzeImageUrl(imageUrl, prompt) {
  const response = await client.chat.completions.create({
    model: 'anthropic/claude-sonnet-4',
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: imageUrl } },
        ],
      },
    ],
  });

  return response.choices[0].message.content;
}

// Base64로 이미지 분석
async function analyzeImageFile(filePath, prompt) {
  const imageBuffer = fs.readFileSync(filePath);
  const base64Image = imageBuffer.toString('base64');
  const mimeType = filePath.endsWith('.png') ? 'image/png' : 'image/jpeg';

  const response = await client.chat.completions.create({
    model: 'anthropic/claude-sonnet-4',
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          {
            type: 'image_url',
            image_url: { url: `data:${mimeType};base64,${base64Image}` },
          },
        ],
      },
    ],
  });

  return response.choices[0].message.content;
}
```

---

## 에러 처리

### 일반적인 에러

```python
def analyze_image_safe(image_path: str, prompt: str) -> str:
    """에러 처리가 포함된 이미지 분석"""
    try:
        # 파일 존재 확인
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"이미지 없음: {image_path}")

        # 파일 크기 확인 (20MB 제한)
        file_size = os.path.getsize(image_path)
        if file_size > 20 * 1024 * 1024:
            raise ValueError("이미지가 너무 큽니다 (20MB 초과)")

        image_base64 = encode_image(image_path)

        response = client.chat.completions.create(
            model="anthropic/claude-sonnet-4",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        )

        return response.choices[0].message.content

    except FileNotFoundError as e:
        return f"파일 에러: {e}"
    except ValueError as e:
        return f"검증 에러: {e}"
    except Exception as e:
        return f"API 에러: {e}"
```

### 지원 형식 확인

```python
SUPPORTED_IMAGE_TYPES = [".png", ".jpg", ".jpeg", ".gif", ".webp"]
SUPPORTED_DOC_TYPES = [".pdf"]

def is_supported_format(file_path: str) -> bool:
    ext = os.path.splitext(file_path)[1].lower()
    return ext in SUPPORTED_IMAGE_TYPES + SUPPORTED_DOC_TYPES
```

---

## 비용 고려사항

### 이미지 토큰 계산

```
이미지 토큰 비용 (대략적):
- 작은 이미지 (< 512px): ~85 토큰
- 중간 이미지 (512-1024px): ~170 토큰
- 큰 이미지 (> 1024px): ~340+ 토큰

PDF 토큰 비용:
- 페이지당 약 ~1000-2000 토큰 (내용에 따라 다름)
```

### 비용 최적화 팁

```python
from PIL import Image

def optimize_image(image_path: str, max_size: int = 1024) -> str:
    """이미지 크기 최적화하여 토큰 절약"""
    img = Image.open(image_path)

    # 크기 조정
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = tuple(int(dim * ratio) for dim in img.size)
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    # 임시 파일로 저장
    import io
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode("utf-8")
```

---

## 핵심 요약

```python
# 이미지 분석 기본 패턴
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "프롬프트"},
            {"type": "image_url", "image_url": {"url": "URL 또는 data:image/..."}}
        ]
    }]
)

# 지원 형식: PNG, JPEG, GIF, WebP, PDF
# 권장 모델: claude-sonnet-4, gpt-4o
# 비용 절약: 이미지 리사이즈 (1024px 이하)
```

---

## 다음 단계

- [[06-cost-management|비용 관리]]
- [[../05-projects|실전 프로젝트]]

---

## 관련 노트

- [[02-models|모델 선택]]
- [[03-openai-sdk|OpenAI SDK]]
- [[../cheatsheet|치트시트]]
