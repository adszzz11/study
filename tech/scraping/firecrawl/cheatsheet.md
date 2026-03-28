# Firecrawl Cheatsheet

> 빠른 참조를 위한 Firecrawl 사용 가이드

---

## 설치

```bash
# Python
pip install firecrawl-py

# Node.js
npm install @mendable/firecrawl-js

# Go
go get github.com/mendableai/firecrawl-go
```

---

## 초기화

```python
# Python
from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")
```

```javascript
// Node.js
import FirecrawlApp from '@mendable/firecrawl-js';
const app = new FirecrawlApp({ apiKey: 'fc-YOUR_API_KEY' });
```

---

## Scrape API

### 기본 스크래핑

```python
result = app.scrape_url("https://example.com")
print(result["markdown"])
```

### 옵션 포함

```python
result = app.scrape_url("https://example.com", {
    "formats": ["markdown", "html", "links"],
    "onlyMainContent": True,
    "excludeTags": ["nav", "footer"],
    "includeTags": ["article", ".content"],
    "waitFor": 3000
})
```

### 스크린샷 캡처

```python
result = app.scrape_url("https://example.com", {
    "formats": ["screenshot"]
})
# result["screenshot"] = base64 encoded image
```

---

## Crawl API

### 동기 크롤링

```python
result = app.crawl_url("https://example.com", {
    "limit": 50,
    "maxDepth": 3,
    "includePaths": ["/docs/*"],
    "excludePaths": ["/admin/*"]
})

for page in result["data"]:
    print(page["metadata"]["sourceURL"])
    print(page["markdown"][:200])
```

### 비동기 크롤링

```python
# 작업 시작
job = app.async_crawl_url("https://example.com", {"limit": 100})
job_id = job["id"]

# 상태 확인
status = app.check_crawl_status(job_id)
print(status["status"])  # "scraping", "completed"

# 결과 가져오기
result = app.get_crawl_status(job_id)
```

---

## Map API

```python
# URL 목록만 가져오기
result = app.map_url("https://example.com")
urls = result["links"]

# 필터링
result = app.map_url("https://example.com", {
    "search": "api",
    "includePaths": ["/docs/*"],
    "limit": 100
})
```

---

## Extract API

### Pydantic 스키마 사용

```python
from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    name: str
    price: float
    features: List[str]

result = app.scrape_url("https://example.com/product", {
    "formats": ["extract"],
    "extract": {
        "schema": Product.model_json_schema()
    }
})

product = Product(**result["extract"])
```

### JSON 스키마 직접 사용

```python
result = app.scrape_url(url, {
    "formats": ["extract"],
    "extract": {
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"}
            }
        }
    }
})
```

### 프롬프트만 사용

```python
result = app.scrape_url(url, {
    "formats": ["extract"],
    "extract": {
        "prompt": "제품명과 가격을 추출해주세요"
    }
})
```

---

## LangChain 통합

```python
from langchain_community.document_loaders import FireCrawlLoader

# Scrape 모드
loader = FireCrawlLoader(
    url="https://example.com",
    api_key="fc-YOUR_API_KEY",
    mode="scrape"
)
docs = loader.load()

# Crawl 모드
loader = FireCrawlLoader(
    url="https://example.com",
    api_key="fc-YOUR_API_KEY",
    mode="crawl",
    params={"limit": 50}
)
docs = loader.load()
```

---

## LlamaIndex 통합

```python
from llama_index.readers.web import FireCrawlWebReader

reader = FireCrawlWebReader(
    api_key="fc-YOUR_API_KEY",
    mode="crawl"
)
documents = reader.load_data(url="https://example.com")
```

---

## 자주 사용하는 옵션

### Scrape 옵션

| 옵션 | 타입 | 설명 |
|------|------|------|
| `formats` | array | `["markdown", "html", "links", "screenshot", "extract"]` |
| `onlyMainContent` | bool | 본문만 추출 (기본: true) |
| `includeTags` | array | 포함할 CSS 선택자 |
| `excludeTags` | array | 제외할 CSS 선택자 |
| `waitFor` | number | JS 실행 대기 (ms) |
| `timeout` | number | 타임아웃 (ms) |

### Crawl 옵션

| 옵션 | 타입 | 설명 |
|------|------|------|
| `limit` | number | 최대 페이지 수 |
| `maxDepth` | number | 크롤링 깊이 |
| `includePaths` | array | 포함할 URL 패턴 |
| `excludePaths` | array | 제외할 URL 패턴 |
| `allowExternalLinks` | bool | 외부 링크 포함 |
| `allowSubdomains` | bool | 서브도메인 포함 |

---

## 에러 핸들링

```python
from firecrawl import FirecrawlApp
from firecrawl.exceptions import FirecrawlError

try:
    result = app.scrape_url(url)
except FirecrawlError as e:
    print(f"Firecrawl 에러: {e}")
except Exception as e:
    print(f"일반 에러: {e}")
```

---

## 캐싱 패턴

```python
import hashlib
import json
import os

def cached_scrape(app, url, cache_dir="./cache"):
    os.makedirs(cache_dir, exist_ok=True)
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_path = f"{cache_dir}/{cache_key}.json"

    if os.path.exists(cache_path):
        with open(cache_path) as f:
            return json.load(f)

    result = app.scrape_url(url)
    with open(cache_path, "w") as f:
        json.dump(result, f)

    return result
```

---

## 비용 계산

```
Scrape: 1 크레딧/페이지
Crawl: 1 크레딧/페이지
Map: 1 크레딧/요청
Extract: 추가 크레딧

Free: 500 크레딧/월
Pro: $19/월, 3,000 크레딧
```

---

## REST API

```bash
# Scrape
curl -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Crawl
curl -X POST https://api.firecrawl.dev/v1/crawl \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "limit": 10}'

# Map
curl -X POST https://api.firecrawl.dev/v1/map \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## 유용한 패턴

### 사이트 구조 먼저 파악

```python
# 1. Map으로 URL 목록
urls = app.map_url(base_url)["links"]

# 2. 필터링
target_urls = [u for u in urls if "/docs/" in u]

# 3. 스크래핑
for url in target_urls:
    result = app.scrape_url(url)
```

### 배치 처리

```python
import time

def batch_scrape(urls, delay=1):
    results = []
    for i, url in enumerate(urls):
        result = app.scrape_url(url)
        results.append(result)
        if (i + 1) % 10 == 0:
            time.sleep(delay)
    return results
```

### RAG 파이프라인

```python
# 수집 → 청킹 → 임베딩 → 벡터 DB
from langchain_community.document_loaders import FireCrawlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

loader = FireCrawlLoader(url=url, mode="crawl")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
chunks = splitter.split_documents(docs)

vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())
```

---

## 링크

- 공식 문서: [docs.firecrawl.dev](https://docs.firecrawl.dev)
- GitHub: [github.com/mendableai/firecrawl](https://github.com/mendableai/firecrawl)
- 대시보드: [firecrawl.dev/app](https://firecrawl.dev/app)
- Playground: [firecrawl.dev/playground](https://firecrawl.dev/playground)
