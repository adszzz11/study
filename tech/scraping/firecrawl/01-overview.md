# Firecrawl 개요

## Firecrawl이란?

Firecrawl은 웹사이트를 **LLM(대규모 언어 모델)이 이해할 수 있는 형식**으로 변환하는 API 서비스이다. 웹 스크래핑의 복잡한 문제들(JavaScript 렌더링, 안티봇, 프록시 등)을 자동으로 처리하여 깨끗한 Markdown이나 구조화된 데이터를 제공한다.

```
웹사이트 → Firecrawl → LLM-Ready Data (Markdown/JSON)
```

---

## 핵심 개념

### 주요 API

| API | 용도 | 사용 사례 |
|-----|------|----------|
| **Scrape** | 단일 URL 스크래핑 | 특정 페이지 내용 추출 |
| **Crawl** | 전체 웹사이트 크롤링 | 문서 사이트 전체 수집 |
| **Map** | 사이트 URL 목록 수집 | 크롤링 전 구조 파악 |
| **Extract** | AI 기반 데이터 추출 | 구조화된 정보 추출 |
| **Search** | 웹 검색 + 스크래핑 | 검색 결과 내용 수집 |

### 동작 원리

```
1. URL 요청
   ↓
2. 헤드리스 브라우저로 페이지 로드
   ↓
3. JavaScript 실행 및 동적 콘텐츠 대기
   ↓
4. HTML → Clean Markdown 변환
   ↓
5. 메타데이터 추출 (제목, 설명, 링크 등)
   ↓
6. 결과 반환
```

### 출력 포맷

```python
{
    "markdown": "# 페이지 제목\n\n본문 내용...",
    "html": "<html>...</html>",
    "metadata": {
        "title": "페이지 제목",
        "description": "페이지 설명",
        "language": "ko",
        "sourceURL": "https://example.com"
    },
    "links": ["https://example.com/page1", "..."],
    "screenshot": "base64_encoded_image"
}
```

---

## 장점

### 1. 복잡한 문제 자동 해결

```python
# 직접 구현 시 필요한 것들
- Selenium/Playwright 설정
- JavaScript 렌더링 대기 로직
- 프록시 풀 관리
- CAPTCHA 우회
- IP 로테이션
- User-Agent 관리

# Firecrawl 사용 시
result = app.scrape_url("https://example.com")  # 끝!
```

### 2. LLM 최적화 출력

- 광고, 네비게이션, 푸터 등 노이즈 자동 제거
- 본문 중심의 깨끗한 Markdown
- 토큰 효율적인 형식

### 3. 다양한 SDK 지원

```python
# Python
from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key="...")
```

```javascript
// Node.js
import FirecrawlApp from '@mendable/firecrawl-js';
const app = new FirecrawlApp({ apiKey: '...' });
```

```go
// Go
import "github.com/mendableai/firecrawl-go"
app := firecrawl.NewFirecrawlApp("...")
```

### 4. 프레임워크 통합

- LangChain: `FireCrawlLoader`
- LlamaIndex: `FireCrawlWebReader`
- 네이티브 지원으로 쉬운 RAG 파이프라인 구축

---

## 단점 및 고려사항

### 1. 비용

```
무료 티어: 500 크레딧/월
Pro: $19/월 (3,000 크레딧)
Scale: 사용량 기반 과금

* 1 Scrape = 1 크레딧
* 1 Crawl = 페이지 수만큼 크레딧
```

### 2. 속도 의존성

- API 서버 응답 속도에 의존
- 대량 크롤링 시 rate limit 고려 필요

### 3. 셀프호스팅 복잡성

- 오픈소스 버전 직접 배포 가능하나 설정 복잡
- 프록시, 브라우저 인프라 직접 관리 필요

---

## 사용 사례

### 1. RAG 시스템 데이터 수집

```python
# 문서 사이트 전체를 벡터 DB에 인덱싱
app = FirecrawlApp(api_key=api_key)
docs = app.crawl_url("https://docs.example.com", {
    "limit": 100,
    "scrapeOptions": {"formats": ["markdown"]}
})

for doc in docs["data"]:
    # 벡터 DB에 저장
    vector_store.add(doc["markdown"], metadata=doc["metadata"])
```

### 2. 경쟁사 모니터링

```python
# 가격 페이지 정기적 스크래핑
competitors = [
    "https://competitor1.com/pricing",
    "https://competitor2.com/pricing"
]

for url in competitors:
    result = app.scrape_url(url, {"formats": ["markdown"]})
    # 변경사항 감지 로직
```

### 3. 콘텐츠 수집 자동화

```python
# 뉴스 사이트에서 기사 수집
result = app.scrape_url(news_url, {
    "formats": ["markdown"],
    "onlyMainContent": True  # 본문만 추출
})
```

### 4. AI 에이전트용 웹 데이터

```python
# LangChain 에이전트에서 웹 정보 활용
from langchain_community.document_loaders import FireCrawlLoader

loader = FireCrawlLoader(
    url="https://example.com",
    api_key=api_key,
    mode="scrape"
)
docs = loader.load()
```

---

## Firecrawl vs 직접 구현

| 항목 | Firecrawl | 직접 구현 (Selenium/Playwright) |
|------|-----------|--------------------------------|
| 초기 설정 | API 키만 필요 | 브라우저, 드라이버 설정 필요 |
| JS 렌더링 | 자동 | 직접 대기 로직 구현 |
| 안티봇 우회 | 내장 | 프록시, User-Agent 직접 관리 |
| 확장성 | 즉시 확장 가능 | 인프라 구축 필요 |
| 비용 | 사용량 과금 | 인프라 비용 |
| 제어 수준 | 제한적 | 완전한 제어 |

---

## 다음 단계

- [[02-ecosystem|에코시스템]] - 관련 기술 및 비교
- [[04-learning/01-scrape|Scrape API 실습]]
