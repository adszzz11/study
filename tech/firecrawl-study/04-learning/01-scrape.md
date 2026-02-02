# Scrape API - 단일 페이지 스크래핑

## 개요

Scrape API는 **단일 URL의 콘텐츠를 추출**하는 가장 기본적인 API이다. JavaScript 렌더링, 프록시, 안티봇 처리를 자동으로 수행하여 깨끗한 Markdown을 반환한다.

```
URL 입력 → Firecrawl 처리 → Markdown/HTML/메타데이터 출력
```

---

## 기본 사용법

### Python

```python
from firecrawl import FirecrawlApp

# 초기화
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# 기본 스크래핑
result = app.scrape_url("https://example.com")

# 결과 확인
print(result["markdown"])
print(result["metadata"])
```

### Node.js

```javascript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({ apiKey: 'fc-YOUR_API_KEY' });

const result = await app.scrapeUrl('https://example.com');
console.log(result.markdown);
```

### REST API

```bash
curl -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }'
```

---

## 결과 구조

```python
{
    "success": True,
    "data": {
        "markdown": "# 페이지 제목\n\n본문 내용...",
        "html": "<html>...</html>",
        "rawHtml": "<html><!-- 원본 HTML -->...</html>",
        "metadata": {
            "title": "페이지 제목",
            "description": "페이지 설명",
            "language": "ko",
            "sourceURL": "https://example.com",
            "statusCode": 200
        },
        "links": [
            "https://example.com/page1",
            "https://example.com/page2"
        ],
        "screenshot": "base64_encoded_image"  # 옵션
    }
}
```

---

## 옵션 설정

### 출력 포맷 선택

```python
# Markdown만 필요한 경우 (기본값)
result = app.scrape_url(url, {
    "formats": ["markdown"]
})

# HTML도 함께 필요한 경우
result = app.scrape_url(url, {
    "formats": ["markdown", "html"]
})

# 스크린샷 포함
result = app.scrape_url(url, {
    "formats": ["markdown", "screenshot"]
})

# 링크 목록 포함
result = app.scrape_url(url, {
    "formats": ["markdown", "links"]
})
```

### 본문만 추출

```python
# 네비게이션, 푸터 등 제외하고 메인 콘텐츠만
result = app.scrape_url(url, {
    "formats": ["markdown"],
    "onlyMainContent": True
})
```

### 특정 태그 포함/제외

```python
# 특정 요소만 추출
result = app.scrape_url(url, {
    "formats": ["markdown"],
    "includeTags": ["article", "main", ".content"]
})

# 특정 요소 제외
result = app.scrape_url(url, {
    "formats": ["markdown"],
    "excludeTags": ["nav", "footer", ".sidebar", "#ads"]
})
```

### JavaScript 실행 대기

```python
# 동적 콘텐츠 로딩 대기
result = app.scrape_url(url, {
    "formats": ["markdown"],
    "waitFor": 5000  # 5초 대기
})
```

---

## 실전 예제

### 예제 1: 블로그 글 수집

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

def scrape_blog_post(url):
    """블로그 글의 본문만 깨끗하게 추출"""
    result = app.scrape_url(url, {
        "formats": ["markdown"],
        "onlyMainContent": True,
        "excludeTags": [".comments", ".related-posts", ".author-bio"]
    })

    return {
        "title": result["metadata"]["title"],
        "content": result["markdown"],
        "url": url
    }

# 사용
post = scrape_blog_post("https://blog.example.com/post-123")
print(post["title"])
print(post["content"])
```

### 예제 2: 제품 페이지 스크래핑

```python
def scrape_product_page(url):
    """제품 정보 추출"""
    result = app.scrape_url(url, {
        "formats": ["markdown", "html"],
        "onlyMainContent": True
    })

    return {
        "markdown": result["markdown"],
        "html": result["html"],
        "metadata": result["metadata"]
    }

# 사용
product = scrape_product_page("https://shop.example.com/product/123")
```

### 예제 3: SPA 페이지 처리

```python
def scrape_spa_page(url):
    """React/Vue/Angular 등 SPA 페이지 스크래핑"""
    result = app.scrape_url(url, {
        "formats": ["markdown"],
        "waitFor": 3000,  # JavaScript 실행 대기
        "onlyMainContent": True
    })

    return result["markdown"]
```

### 예제 4: 스크린샷 캡처

```python
import base64

def capture_screenshot(url, output_path):
    """페이지 스크린샷 저장"""
    result = app.scrape_url(url, {
        "formats": ["screenshot"]
    })

    # Base64 디코딩 후 파일 저장
    screenshot_data = base64.b64decode(result["screenshot"])
    with open(output_path, "wb") as f:
        f.write(screenshot_data)

    return output_path

# 사용
capture_screenshot("https://example.com", "page_screenshot.png")
```

---

## 에러 핸들링

```python
from firecrawl import FirecrawlApp
from firecrawl.exceptions import FirecrawlError

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

def safe_scrape(url):
    """에러 처리가 포함된 스크래핑"""
    try:
        result = app.scrape_url(url, {
            "formats": ["markdown"],
            "timeout": 30000
        })

        if result.get("success"):
            return result["markdown"]
        else:
            print(f"스크래핑 실패: {result.get('error')}")
            return None

    except FirecrawlError as e:
        print(f"Firecrawl 에러: {e}")
        return None
    except Exception as e:
        print(f"예상치 못한 에러: {e}")
        return None

# 사용
content = safe_scrape("https://example.com")
if content:
    print(content)
```

---

## 배치 스크래핑

```python
import asyncio
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

def batch_scrape(urls):
    """여러 URL 순차 스크래핑"""
    results = []

    for url in urls:
        try:
            result = app.scrape_url(url, {"formats": ["markdown"]})
            results.append({
                "url": url,
                "success": True,
                "content": result["markdown"]
            })
        except Exception as e:
            results.append({
                "url": url,
                "success": False,
                "error": str(e)
            })

    return results

# 사용
urls = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
]
results = batch_scrape(urls)
```

---

## 옵션 전체 목록

| 옵션 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `formats` | array | `["markdown"]` | 출력 포맷 |
| `onlyMainContent` | boolean | `true` | 본문만 추출 |
| `includeTags` | array | `[]` | 포함할 HTML 요소 |
| `excludeTags` | array | `[]` | 제외할 HTML 요소 |
| `waitFor` | number | `0` | JS 실행 대기(ms) |
| `timeout` | number | `30000` | 타임아웃(ms) |
| `mobile` | boolean | `false` | 모바일 뷰포트 |
| `skipTlsVerification` | boolean | `false` | TLS 검증 스킵 |

---

## 팁과 주의사항

### 크레딧 절약

```python
# 필요한 포맷만 요청 (각 포맷 추가 시 크레딧 소모)
result = app.scrape_url(url, {
    "formats": ["markdown"]  # screenshot, html 제외
})
```

### 동적 콘텐츠 처리

```python
# 무한 스크롤 페이지는 waitFor 활용
result = app.scrape_url(url, {
    "waitFor": 5000  # 충분한 대기 시간
})
```

### 대용량 페이지

```python
# 긴 페이지는 특정 부분만 추출
result = app.scrape_url(url, {
    "includeTags": ["article"],  # 본문만
    "excludeTags": [".comments"]  # 댓글 제외
})
```

---

## 다음 단계

- [[02-extract|Extract API]] - AI 기반 구조화 데이터 추출
- [[03-crawl|Crawl API]] - 웹사이트 전체 크롤링
