# Crawl API - 웹사이트 전체 크롤링

## 개요

Crawl API는 **시작 URL부터 링크를 따라가며 웹사이트 전체를 크롤링**하는 API이다. 문서 사이트, 블로그 전체 글, 쇼핑몰 제품 목록 등을 한 번에 수집할 때 사용한다.

```
시작 URL → 링크 탐색 → 각 페이지 스크래핑 → 전체 데이터 반환
```

---

## 기본 사용법

### 동기 방식 (작은 사이트)

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# 기본 크롤링
result = app.crawl_url("https://docs.example.com", {
    "limit": 10  # 최대 10페이지
})

# 결과 확인
for page in result["data"]:
    print(f"URL: {page['metadata']['sourceURL']}")
    print(f"Content: {page['markdown'][:200]}...")
    print("---")
```

### 비동기 방식 (큰 사이트)

```python
# 크롤링 작업 시작
crawl_status = app.async_crawl_url("https://docs.example.com", {
    "limit": 100
})

job_id = crawl_status["id"]
print(f"Job ID: {job_id}")

# 상태 확인 (폴링)
import time

while True:
    status = app.check_crawl_status(job_id)
    print(f"Status: {status['status']}, Pages: {status.get('completed', 0)}")

    if status["status"] == "completed":
        break

    time.sleep(5)

# 결과 가져오기
result = app.get_crawl_status(job_id)
print(f"총 {len(result['data'])}개 페이지 크롤링 완료")
```

### Node.js

```javascript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({ apiKey: 'fc-YOUR_API_KEY' });

// 동기 크롤링
const result = await app.crawlUrl('https://docs.example.com', {
  limit: 10
});

// 비동기 크롤링
const job = await app.asyncCrawlUrl('https://docs.example.com', {
  limit: 100
});

// 상태 확인
const status = await app.checkCrawlStatus(job.id);
```

---

## 주요 옵션

### 크롤링 범위 제어

```python
result = app.crawl_url("https://example.com", {
    # 최대 페이지 수
    "limit": 50,

    # 크롤링 깊이 (시작 URL부터의 링크 거리)
    "maxDepth": 3,

    # 특정 경로만 포함
    "includePaths": ["/docs/*", "/blog/*"],

    # 특정 경로 제외
    "excludePaths": ["/admin/*", "/login"],

    # 외부 링크 따라가기
    "allowExternalLinks": False,

    # 서브도메인 포함
    "allowSubdomains": False
})
```

### 스크래핑 옵션

```python
result = app.crawl_url("https://example.com", {
    "limit": 50,
    "scrapeOptions": {
        "formats": ["markdown"],
        "onlyMainContent": True,
        "excludeTags": ["nav", "footer", ".sidebar"]
    }
})
```

### 속도 제어

```python
result = app.crawl_url("https://example.com", {
    "limit": 100,
    # 동시 요청 수 (기본값: 5)
    "maxConcurrency": 10
})
```

---

## 실전 예제

### 예제 1: 문서 사이트 전체 수집

```python
def crawl_documentation(base_url, output_dir):
    """문서 사이트 전체를 마크다운으로 저장"""
    import os

    result = app.crawl_url(base_url, {
        "limit": 200,
        "includePaths": ["/docs/*", "/guide/*", "/api/*"],
        "scrapeOptions": {
            "formats": ["markdown"],
            "onlyMainContent": True
        }
    })

    os.makedirs(output_dir, exist_ok=True)

    for page in result["data"]:
        # URL에서 파일명 생성
        url = page["metadata"]["sourceURL"]
        filename = url.replace(base_url, "").replace("/", "_") + ".md"
        filename = filename.lstrip("_") or "index.md"

        # 파일 저장
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {page['metadata']['title']}\n\n")
            f.write(f"Source: {url}\n\n")
            f.write(page["markdown"])

        print(f"저장: {filepath}")

    return len(result["data"])

# 사용
count = crawl_documentation(
    "https://docs.example.com",
    "./collected_docs"
)
print(f"총 {count}개 문서 저장 완료")
```

### 예제 2: 블로그 아카이브

```python
def archive_blog(blog_url):
    """블로그 전체 글 아카이브"""
    result = app.crawl_url(blog_url, {
        "limit": 500,
        "includePaths": ["/posts/*", "/blog/*", "/article/*"],
        "excludePaths": ["/tag/*", "/category/*", "/author/*"],
        "scrapeOptions": {
            "formats": ["markdown"],
            "onlyMainContent": True,
            "excludeTags": [".comments", ".related-posts"]
        }
    })

    posts = []
    for page in result["data"]:
        posts.append({
            "title": page["metadata"].get("title", "Untitled"),
            "url": page["metadata"]["sourceURL"],
            "content": page["markdown"],
            "description": page["metadata"].get("description", "")
        })

    return posts

# 사용
posts = archive_blog("https://blog.example.com")
print(f"총 {len(posts)}개 글 수집")
```

### 예제 3: 제품 카탈로그 수집

```python
def crawl_product_catalog(shop_url):
    """쇼핑몰 제품 목록 수집"""
    result = app.crawl_url(shop_url, {
        "limit": 1000,
        "includePaths": ["/products/*", "/item/*"],
        "excludePaths": ["/cart", "/checkout", "/account/*"],
        "scrapeOptions": {
            "formats": ["markdown", "extract"],
            "extract": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "number"},
                        "category": {"type": "string"},
                        "in_stock": {"type": "boolean"}
                    }
                }
            }
        }
    })

    products = []
    for page in result["data"]:
        if "extract" in page:
            products.append({
                "url": page["metadata"]["sourceURL"],
                **page["extract"]
            })

    return products
```

### 예제 4: RAG용 데이터 수집

```python
def collect_for_rag(urls, vector_store):
    """RAG 시스템용 데이터 수집 및 인덱싱"""
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    for url in urls:
        result = app.crawl_url(url, {
            "limit": 100,
            "scrapeOptions": {
                "formats": ["markdown"],
                "onlyMainContent": True
            }
        })

        for page in result["data"]:
            # 청킹
            chunks = splitter.split_text(page["markdown"])

            # 벡터 저장소에 추가
            for i, chunk in enumerate(chunks):
                vector_store.add_texts(
                    texts=[chunk],
                    metadatas=[{
                        "source": page["metadata"]["sourceURL"],
                        "title": page["metadata"].get("title", ""),
                        "chunk_index": i
                    }]
                )

        print(f"Indexed {len(result['data'])} pages from {url}")
```

---

## 웹훅 (Webhook) 활용

```python
# 크롤링 완료 시 웹훅으로 알림 받기
result = app.async_crawl_url("https://docs.example.com", {
    "limit": 100,
    "webhook": "https://your-server.com/webhook/firecrawl"
})

print(f"Job started: {result['id']}")
# 완료되면 웹훅으로 결과 전송됨
```

### 웹훅 서버 예시 (FastAPI)

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook/firecrawl")
async def firecrawl_webhook(request: Request):
    data = await request.json()

    if data["status"] == "completed":
        print(f"크롤링 완료: {len(data['data'])}개 페이지")
        # 데이터 처리 로직

    return {"status": "received"}
```

---

## 크롤링 전략

### 1. 점진적 크롤링

```python
def incremental_crawl(base_url, last_crawl_urls):
    """이전에 수집한 URL 제외하고 새로운 페이지만 크롤링"""
    result = app.crawl_url(base_url, {
        "limit": 500,
        "scrapeOptions": {"formats": ["markdown"]}
    })

    new_pages = []
    for page in result["data"]:
        url = page["metadata"]["sourceURL"]
        if url not in last_crawl_urls:
            new_pages.append(page)

    return new_pages
```

### 2. 우선순위 크롤링

```python
def priority_crawl(base_url):
    """중요 페이지 먼저 크롤링"""
    # 1단계: 메인 페이지들
    main_result = app.crawl_url(base_url, {
        "limit": 50,
        "maxDepth": 1,
        "includePaths": ["/docs/*", "/guide/*"]
    })

    # 2단계: 상세 페이지들
    detail_result = app.crawl_url(base_url, {
        "limit": 200,
        "maxDepth": 3,
        "includePaths": ["/api/*", "/reference/*"]
    })

    return main_result["data"] + detail_result["data"]
```

---

## 옵션 전체 목록

| 옵션 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `limit` | number | 10000 | 최대 크롤링 페이지 수 |
| `maxDepth` | number | 무제한 | 크롤링 깊이 |
| `includePaths` | array | [] | 포함할 URL 패턴 |
| `excludePaths` | array | [] | 제외할 URL 패턴 |
| `allowExternalLinks` | boolean | false | 외부 링크 포함 |
| `allowSubdomains` | boolean | false | 서브도메인 포함 |
| `maxConcurrency` | number | 5 | 동시 요청 수 |
| `webhook` | string | null | 완료 알림 URL |
| `scrapeOptions` | object | {} | 각 페이지 스크래핑 옵션 |

---

## 주의사항

### 크레딧 소비

```
1 Crawl = 크롤링된 페이지 수만큼 크레딧

예: limit=100으로 50페이지 크롤링 시 = 50 크레딧
```

### Rate Limit

```python
# 큰 사이트는 비동기 방식 사용
# 동기 방식은 타임아웃 위험

# 권장: 100페이지 이상은 비동기
if expected_pages > 100:
    job = app.async_crawl_url(url, options)
else:
    result = app.crawl_url(url, options)
```

### 예의 바른 크롤링

```python
# robots.txt 존중 (기본 동작)
# 너무 빠른 크롤링 자제
result = app.crawl_url(url, {
    "limit": 100,
    "maxConcurrency": 3  # 동시 요청 줄이기
})
```

---

## 에러 핸들링

```python
def safe_crawl(url, options):
    """에러 처리가 포함된 크롤링"""
    try:
        result = app.crawl_url(url, options)

        if not result.get("success"):
            print(f"크롤링 실패: {result.get('error')}")
            return []

        # 부분 실패 확인
        failed_pages = [
            p for p in result.get("data", [])
            if p.get("metadata", {}).get("statusCode") != 200
        ]

        if failed_pages:
            print(f"경고: {len(failed_pages)}개 페이지 실패")

        return result["data"]

    except Exception as e:
        print(f"크롤링 에러: {e}")
        return []
```

---

## 다음 단계

- [[04-map|Map API]] - 크롤링 전 사이트 구조 파악
- [[05-langchain|LangChain 통합]] - 수집 데이터로 RAG 구축
