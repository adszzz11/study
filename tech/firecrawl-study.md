# Firecrawl 심층 스터디 가이드

> **한 줄 정의**: 웹사이트 전체를 LLM이 바로 사용할 수 있는 Markdown/구조화 데이터로 변환하는 Web Data API

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**3줄 요약**:
1. URL 하나로 웹페이지를 깔끔한 Markdown으로 변환 - RAG 파이프라인에 최적화
2. 전체 웹사이트 크롤링(Crawl), 사이트맵 추출(Map), AI 구조화 추출(Extract) 지원
3. JavaScript 렌더링, 프록시, 안티봇 우회를 자동 처리

**핵심 키워드**: `#웹스크래핑` `#RAG` `#LLM전처리` `#크롤링` `#API`

**Firecrawl의 핵심 기능**:

| 기능 | 설명 | 용도 |
|------|------|------|
| **Scrape** | 단일 URL → Markdown/JSON | 개별 페이지 데이터 수집 |
| **Crawl** | 웹사이트 전체 크롤링 | 전체 사이트 인덱싱 |
| **Map** | 사이트 URL 목록 추출 | 크롤링 대상 파악 |
| **Extract** | AI로 구조화 데이터 추출 | 특정 정보 추출 |
| **Search** | 웹 검색 + 콘텐츠 추출 | 실시간 정보 수집 |

### 1.2 Quick Start (30초 체험)

```bash
# 1. 설치
pip install firecrawl-py

# 또는 Node.js
npm install @mendable/firecrawl-js
```

**Python 예제**:
```python
from firecrawl import FirecrawlApp

# API 키로 초기화
app = FirecrawlApp(api_key="fc-YOUR-API-KEY")

# 단일 페이지 스크래핑
result = app.scrape_url("https://example.com")
print(result["markdown"])  # 깔끔한 Markdown

# 구조화 데이터 추출
structured = app.scrape_url(
    "https://news.ycombinator.com",
    params={
        "formats": ["extract"],
        "extract": {
            "schema": {
                "type": "object",
                "properties": {
                    "top_stories": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            },
            "prompt": "상위 5개 뉴스 제목 추출"
        }
    }
)
print(structured["extract"])
```

**cURL로 바로 테스트**:
```bash
curl -X POST 'https://api.firecrawl.dev/v1/scrape' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer fc-YOUR-API-KEY' \
  -d '{
    "url": "https://example.com",
    "formats": ["markdown", "html"]
  }'
```

### 1.3 왜 Firecrawl인가?

**장점**:
- **LLM 최적화 출력**: 깔끔한 Markdown으로 토큰 효율적
- **JavaScript 렌더링**: 동적 웹페이지도 완벽 처리
- **인프라 불필요**: 프록시, 안티봇, 브라우저 관리 자동
- **빠른 속도**: 결과 1초 이내, 캐싱 지원
- **96% 웹 커버리지**: 대부분의 웹사이트 지원

**단점**:
- API 비용 (크레딧 기반)
- Self-hosted 버전은 일부 기능 제한
- 매우 복잡한 인터랙션은 미지원

**주요 사용 사례**:
- RAG 파이프라인 문서 수집
- 경쟁사/시장 모니터링
- 콘텐츠 수집 및 분석
- 검색 엔진 구축
- AI 에이전트 웹 브라우징

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    Firecrawl 생태계                          │
├─────────────────────────────────────────────────────────────┤
│  [Core APIs]                                                 │
│  ├── /scrape: 단일 URL 스크래핑                              │
│  ├── /crawl: 웹사이트 전체 크롤링 (비동기)                    │
│  ├── /map: 사이트 URL 목록 추출                              │
│  ├── /extract: AI 기반 구조화 추출                           │
│  └── /search: 웹 검색 + 콘텐츠                               │
│                                                              │
│  [출력 포맷]                                                 │
│  ├── markdown: LLM 친화적 텍스트                             │
│  ├── html: 원본 HTML                                         │
│  ├── links: 페이지 내 링크                                   │
│  ├── screenshot: 페이지 스크린샷                              │
│  └── extract: AI 구조화 데이터                               │
│                                                              │
│  [SDKs]                                                      │
│  ├── Python: firecrawl-py                                    │
│  ├── Node.js: @mendable/firecrawl-js                         │
│  ├── Go: firecrawl-go                                        │
│  └── Rust: firecrawl-rs                                      │
│                                                              │
│  [통합]                                                      │
│  ├── LangChain: FireCrawlLoader                              │
│  ├── LlamaIndex: FireCrawlWebReader                          │
│  ├── n8n, Zapier: 노코드 통합                                │
│  └── Lovable: AI 앱 빌더                                     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **RAG 프레임워크** | LangChain, LlamaIndex | 문서 로딩 및 검색 |
| **벡터 DB** | Pinecone, Qdrant, Chroma | 임베딩 저장 |
| **LLM** | OpenAI, Claude, Gemini | 질의응답, 분석 |
| **워크플로우** | n8n, Zapier, Prefect | 자동화 |
| **저장소** | Supabase, PostgreSQL | 데이터 저장 |

### 2.3 경쟁/대안 기술 비교

| 기준 | Firecrawl | Crawl4AI | Apify | Jina Reader |
|------|-----------|----------|-------|-------------|
| **접근 방식** | API 중심 | 로컬 우선 | Actor 기반 | URL prefix |
| **Self-hosted** | 부분 지원 | 완전 지원 | 불가 | 불가 |
| **LLM 출력** | Markdown | Markdown | 다양 | Markdown |
| **AI 추출** | 내장 | 외부 연동 | Actor별 | 없음 |
| **가격** | 크레딧 기반 | 무료 | Actor별 | 무료 티어 |
| **GitHub Stars** | 42K+ | 58K+ | - | 19K+ |

**선택 가이드**:
- **Firecrawl**: 빠른 API 기반 스크래핑, RAG 파이프라인
- **Crawl4AI**: 데이터 주권 필요, Self-hosted 선호
- **Apify**: 특정 사이트용 미리 만들어진 스크레이퍼
- **Jina Reader**: 가장 간단한 URL → Markdown 변환

### 2.4 최신 트렌드 및 동향 (2025)

- **42K+ GitHub Stars**: 빠르게 성장하는 커뮤니티
- **FIRE-1 AI Agent**: 지능형 네비게이션 에이전트 (실험적)
- **2일 캐싱**: 동일 페이지 재요청 시 5배 빠른 응답
- **LangChain/LlamaIndex 네이티브 통합**: RAG 파이프라인 표준화
- **Y Combinator 지원**: 스타트업 성장세 지속

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [docs.firecrawl.dev](https://docs.firecrawl.dev/) | 메인 문서 |
| 🟢 GitHub | [github.com/mendableai/firecrawl](https://github.com/mendableai/firecrawl) | 소스 코드 |
| 🟢 대시보드 | [firecrawl.dev](https://www.firecrawl.dev/) | API 키 발급 |
| 🟡 API Reference | [docs.firecrawl.dev/api-reference](https://docs.firecrawl.dev/api-reference) | API 상세 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [Firecrawl Quickstart](https://docs.firecrawl.dev/introduction) - 공식 시작 가이드
- [Scrape Endpoint Tutorial](https://www.firecrawl.dev/blog/mastering-firecrawl-scrape-endpoint) - Scrape 마스터

**🟡 중급**:
- [Crawl Endpoint Guide](https://www.firecrawl.dev/blog/mastering-the-crawl-endpoint-in-firecrawl) - 크롤링 심화
- [LangChain Integration](https://python.langchain.com/docs/integrations/document_loaders/firecrawl) - RAG 연동

**🔴 고급**:
- [Self-hosting Guide](https://docs.firecrawl.dev/contributing/self-host) - 자체 호스팅
- [Extract API](https://docs.firecrawl.dev/features/extract) - AI 추출

### 3.3 커뮤니티 및 질문할 곳

- **GitHub Issues**: [mendableai/firecrawl/issues](https://github.com/mendableai/firecrawl/issues)
- **Discord**: Firecrawl 공식 커뮤니티
- **Twitter/X**: @fiaboringai

### 3.4 실무 예제/오픈소스 프로젝트

- [Firecrawl Examples](https://github.com/mendableai/firecrawl/tree/main/examples)
- [LangChain Cookbook](https://python.langchain.com/docs/integrations/document_loaders/firecrawl)

---

## Part 4: 상세 학습 로드맵

### 4.1 Scrape API - 단일 페이지 스크래핑

📌 **핵심 개념**

Scrape API는 단일 URL을 Markdown, HTML, 스크린샷 등으로 변환합니다. 가장 기본적이고 많이 사용하는 API입니다.

💻 **코드 예제: 다양한 옵션**

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR-API-KEY")

# 1. 기본 스크래핑 (Markdown)
result = app.scrape_url("https://example.com")
print(result["markdown"])

# 2. 다양한 포맷 요청
result = app.scrape_url(
    "https://example.com",
    params={
        "formats": ["markdown", "html", "links", "screenshot"]
    }
)

print("Markdown:", result["markdown"][:500])
print("HTML:", result["html"][:500])
print("Links:", result["links"])
print("Screenshot:", result["screenshot"])  # base64

# 3. 대기 옵션 (JavaScript 렌더링)
result = app.scrape_url(
    "https://spa-website.com",
    params={
        "waitFor": 3000,  # 3초 대기
        "formats": ["markdown"]
    }
)

# 4. 특정 요소만 포함/제외
result = app.scrape_url(
    "https://news.example.com",
    params={
        "includeTags": ["article", "h1", "p"],
        "excludeTags": ["nav", "footer", "aside"],
        "formats": ["markdown"]
    }
)

# 5. 페이지 액션 수행 (스크롤, 클릭 등)
result = app.scrape_url(
    "https://infinite-scroll.com",
    params={
        "actions": [
            {"type": "scroll", "direction": "down", "amount": 2000},
            {"type": "wait", "milliseconds": 1000},
            {"type": "scroll", "direction": "down", "amount": 2000}
        ],
        "formats": ["markdown"]
    }
)
```

**Node.js 버전**:
```javascript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({ apiKey: 'fc-YOUR-API-KEY' });

const result = await app.scrapeUrl('https://example.com', {
    formats: ['markdown', 'html'],
    waitFor: 2000
});

console.log(result.markdown);
```

✅ **체크포인트**
- [ ] 기본 Scrape API를 호출할 수 있는가?
- [ ] 다양한 출력 포맷을 요청할 수 있는가?
- [ ] `waitFor`와 `actions`를 사용할 수 있는가?

⚠️ **흔한 실수**
- `formats`를 지정하지 않으면 markdown만 반환
- JavaScript 사이트는 `waitFor` 필요
- 크레딧: 1 페이지 = 1 크레딧

🔗 **더 알아보기**: [Scrape API](https://docs.firecrawl.dev/features/scrape)

---

### 4.2 Extract API - AI 구조화 추출

📌 **핵심 개념**

Extract API는 LLM을 사용하여 페이지에서 특정 데이터를 구조화된 형태로 추출합니다. JSON 스키마로 출력 형식을 정의합니다.

💻 **코드 예제: 구조화 추출**

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR-API-KEY")

# 1. 간단한 스키마 추출
result = app.scrape_url(
    "https://news.ycombinator.com",
    params={
        "formats": ["extract"],
        "extract": {
            "schema": {
                "type": "object",
                "properties": {
                    "top_stories": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                                "points": {"type": "integer"}
                            }
                        }
                    }
                }
            },
            "prompt": "상위 5개 뉴스의 제목, URL, 포인트 추출"
        }
    }
)

print(result["extract"]["top_stories"])

# 2. 상품 정보 추출
product_result = app.scrape_url(
    "https://shop.example.com/product/123",
    params={
        "formats": ["extract"],
        "extract": {
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "price": {"type": "number"},
                    "currency": {"type": "string"},
                    "availability": {"type": "boolean"},
                    "rating": {"type": "number"},
                    "review_count": {"type": "integer"},
                    "features": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["name", "price"]
            }
        }
    }
)

product = product_result["extract"]
print(f"{product['name']}: {product['currency']}{product['price']}")

# 3. 여러 페이지에서 추출
urls = [
    "https://example.com/product/1",
    "https://example.com/product/2",
    "https://example.com/product/3"
]

all_products = []
for url in urls:
    result = app.scrape_url(url, params={
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
    all_products.append(result["extract"])

print(all_products)
```

**Pydantic 스키마 사용**:
```python
from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    features: List[str] = []

result = app.scrape_url(
    "https://shop.example.com/product",
    params={
        "formats": ["extract"],
        "extract": {
            "schema": Product.model_json_schema()
        }
    }
)
```

✅ **체크포인트**
- [ ] JSON 스키마로 추출 형식을 정의할 수 있는가?
- [ ] 중첩 객체와 배열을 추출할 수 있는가?
- [ ] prompt를 활용해 추출 정확도를 높일 수 있는가?

⚠️ **흔한 실수**
- 스키마가 너무 복잡하면 추출 실패 가능
- `required` 필드 지정으로 필수 데이터 보장
- Extract는 추가 크레딧 소비 가능

🔗 **더 알아보기**: [Extract API](https://docs.firecrawl.dev/features/extract)

---

### 4.3 Crawl API - 웹사이트 전체 크롤링

📌 **핵심 개념**

Crawl API는 시작 URL에서 링크를 따라가며 전체 웹사이트를 크롤링합니다. 비동기로 실행되며, 결과를 폴링하거나 웹훅으로 받습니다.

💻 **코드 예제: 전체 사이트 크롤링**

```python
from firecrawl import FirecrawlApp
import time

app = FirecrawlApp(api_key="fc-YOUR-API-KEY")

# 1. 크롤링 시작
crawl_response = app.crawl_url(
    "https://docs.example.com",
    params={
        "limit": 100,              # 최대 100페이지
        "maxDepth": 3,             # 최대 깊이 3
        "includePaths": ["/docs/*"],  # 특정 경로만
        "excludePaths": ["/blog/*"],  # 제외할 경로
        "formats": ["markdown"]
    },
    poll_interval=5  # 5초마다 상태 확인
)

# 결과 확인 (동기 방식 - 완료까지 대기)
print(f"총 {len(crawl_response['data'])} 페이지 크롤링")

for page in crawl_response['data']:
    print(f"URL: {page['metadata']['url']}")
    print(f"Title: {page['metadata'].get('title', 'N/A')}")
    print(f"Content: {page['markdown'][:200]}...")
    print("---")

# 2. 비동기 방식 (직접 폴링)
crawl_id = app.async_crawl_url(
    "https://example.com",
    params={"limit": 50}
)

print(f"Crawl started: {crawl_id}")

# 상태 확인 루프
while True:
    status = app.check_crawl_status(crawl_id)
    print(f"Status: {status['status']}, Pages: {len(status.get('data', []))}")

    if status['status'] == 'completed':
        break

    time.sleep(5)

# 최종 결과
final_result = app.check_crawl_status(crawl_id)
print(f"Crawl complete: {len(final_result['data'])} pages")

# 3. 웹훅으로 결과 받기
app.crawl_url(
    "https://example.com",
    params={
        "limit": 100,
        "webhook": "https://your-server.com/webhook"
    }
)
# 완료 시 웹훅으로 결과 전송
```

**크롤링 필터링**:
```python
# URL 패턴으로 필터링
result = app.crawl_url(
    "https://example.com",
    params={
        "includePaths": [
            "/products/*",
            "/categories/*"
        ],
        "excludePaths": [
            "/admin/*",
            "/login"
        ],
        "limit": 200
    }
)

# 정규식 사용
result = app.crawl_url(
    "https://example.com",
    params={
        "allowBackwardLinks": False,  # 상위 경로 링크 제외
        "allowExternalLinks": False,  # 외부 링크 제외
        "limit": 100
    }
)
```

✅ **체크포인트**
- [ ] Crawl API로 웹사이트를 크롤링할 수 있는가?
- [ ] `limit`, `maxDepth`, `includePaths`를 활용할 수 있는가?
- [ ] 비동기 크롤링과 폴링을 구현할 수 있는가?

⚠️ **흔한 실수**
- `limit` 없이 크롤링하면 크레딧 과다 소비
- 대형 사이트는 웹훅 방식 권장
- `maxDepth`가 너무 깊으면 불필요한 페이지 포함

🔗 **더 알아보기**: [Crawl API](https://docs.firecrawl.dev/features/crawl)

---

### 4.4 Map API - 사이트 URL 목록 추출

📌 **핵심 개념**

Map API는 웹사이트의 모든 URL을 빠르게 추출합니다. 크롤링 전에 대상 페이지를 파악하는 데 유용합니다.

💻 **코드 예제: 사이트맵 추출**

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR-API-KEY")

# 1. 기본 맵핑
map_result = app.map_url("https://docs.example.com")

print(f"총 {len(map_result['links'])}개 URL 발견")
for url in map_result['links'][:10]:
    print(url)

# 2. 특정 경로 필터링
map_result = app.map_url(
    "https://example.com",
    params={
        "includePaths": ["/blog/*"],
        "limit": 500
    }
)

blog_urls = map_result['links']
print(f"블로그 포스트: {len(blog_urls)}개")

# 3. Map + Crawl 조합
# 먼저 URL 목록 확인
map_result = app.map_url("https://docs.example.com")
total_pages = len(map_result['links'])

print(f"예상 크롤링 페이지: {total_pages}")
print(f"예상 크레딧: {total_pages}")

# 확인 후 크롤링
if total_pages < 100:  # 100페이지 이하면 진행
    crawl_result = app.crawl_url(
        "https://docs.example.com",
        params={"limit": total_pages}
    )

# 4. 사이트맵 기반 크롤링
map_result = app.map_url("https://example.com")

# 특정 패턴의 URL만 크롤링
product_urls = [url for url in map_result['links'] if '/product/' in url]

for url in product_urls[:10]:  # 샘플 10개만
    result = app.scrape_url(url, params={"formats": ["extract"]})
    print(result["extract"])
```

✅ **체크포인트**
- [ ] Map API로 사이트 URL을 추출할 수 있는가?
- [ ] 크롤링 전에 비용을 예측할 수 있는가?
- [ ] Map + Scrape 조합으로 선택적 크롤링을 할 수 있는가?

⚠️ **흔한 실수**
- Map은 크레딧 소비가 적음 (크롤링 전 확인용)
- 모든 URL이 공개 접근 가능한 것은 아님

🔗 **더 알아보기**: [Map API](https://docs.firecrawl.dev/features/map)

---

### 4.5 LangChain/LlamaIndex 통합

📌 **핵심 개념**

Firecrawl은 LangChain, LlamaIndex와 네이티브 통합되어 RAG 파이프라인 구축이 간편합니다.

💻 **코드 예제: LangChain 통합**

```python
from langchain_community.document_loaders import FireCrawlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Firecrawl로 문서 로드
loader = FireCrawlLoader(
    api_key="fc-YOUR-API-KEY",
    url="https://docs.example.com",
    mode="crawl",  # "scrape" 또는 "crawl"
    params={
        "limit": 50,
        "formats": ["markdown"]
    }
)

documents = loader.load()
print(f"로드된 문서: {len(documents)}개")

# 2. 텍스트 분할
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)
print(f"청크 수: {len(chunks)}")

# 3. 벡터 스토어 생성
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./docs_db"
)

# 4. RAG 체인 구성
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4})
)

# 5. 질의응답
answer = qa_chain.run("이 문서의 주요 기능은 무엇인가요?")
print(answer)
```

**LlamaIndex 통합**:
```python
from llama_index.readers.web import FireCrawlWebReader
from llama_index.core import VectorStoreIndex

# 문서 로드
reader = FireCrawlWebReader(
    api_key="fc-YOUR-API-KEY",
    mode="crawl",
    params={"limit": 30}
)

documents = reader.load_data(url="https://docs.example.com")

# 인덱스 생성
index = VectorStoreIndex.from_documents(documents)

# 쿼리
query_engine = index.as_query_engine()
response = query_engine.query("주요 API 엔드포인트를 설명해주세요")
print(response)
```

✅ **체크포인트**
- [ ] FireCrawlLoader로 문서를 로드할 수 있는가?
- [ ] 벡터 스토어에 임베딩을 저장할 수 있는가?
- [ ] RAG 체인을 구성할 수 있는가?

⚠️ **흔한 실수**
- `mode="crawl"` vs `mode="scrape"` 구분
- 청크 크기는 LLM 컨텍스트 제한 고려
- 대규모 크롤링은 비동기 처리 권장

🔗 **더 알아보기**: [LangChain Integration](https://python.langchain.com/docs/integrations/document_loaders/firecrawl)

---

### 4.6 캐싱과 비용 최적화

📌 **핵심 개념**

Firecrawl은 2일간 캐싱을 제공하며, 동일 페이지 재요청 시 빠르게 응답합니다.

💻 **코드 예제: 캐싱 활용**

```python
from firecrawl import FirecrawlApp
import time

app = FirecrawlApp(api_key="fc-YOUR-API-KEY")

# 1. 첫 번째 요청 (크레딧 소비)
start = time.time()
result1 = app.scrape_url("https://example.com")
print(f"첫 요청: {time.time() - start:.2f}초")

# 2. 동일 요청 (캐시 사용, 더 빠름)
start = time.time()
result2 = app.scrape_url("https://example.com")
print(f"캐시 요청: {time.time() - start:.2f}초")

# 3. 캐시 무시 (항상 새로 스크래핑)
result3 = app.scrape_url(
    "https://example.com",
    params={
        "skipCache": True  # 캐시 무시
    }
)
```

**비용 최적화 전략**:
```python
# 1. Map으로 먼저 확인
map_result = app.map_url("https://example.com")
total = len(map_result['links'])
print(f"예상 비용: {total} 크레딧")

# 2. 필요한 페이지만 필터링
target_urls = [
    url for url in map_result['links']
    if '/product/' in url and '/reviews' not in url
]
print(f"최적화 후: {len(target_urls)} 크레딧")

# 3. 필요한 포맷만 요청
result = app.scrape_url(
    "https://example.com",
    params={
        "formats": ["markdown"],  # screenshot 제외
        "excludeTags": ["nav", "footer", "script"]  # 불필요한 태그 제외
    }
)

# 4. 배치 처리로 효율화
from concurrent.futures import ThreadPoolExecutor

def scrape_url(url):
    return app.scrape_url(url, params={"formats": ["markdown"]})

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(scrape_url, target_urls[:20]))
```

**크레딧 사용량 모니터링**:
```python
# API 응답에서 크레딧 정보 확인
result = app.scrape_url("https://example.com")

# 계정 크레딧 확인 (API 키로)
# 대시보드: https://firecrawl.dev/dashboard
```

✅ **체크포인트**
- [ ] 캐싱이 언제 적용되는지 이해하는가?
- [ ] Map으로 비용을 예측할 수 있는가?
- [ ] 필터링과 포맷 선택으로 비용을 줄일 수 있는가?

⚠️ **흔한 실수**
- 캐시는 2일 후 만료
- Extract는 추가 크레딧 소비
- 대규모 크롤링 전 Map으로 확인

🔗 **더 알아보기**: [Pricing](https://www.firecrawl.dev/pricing)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | 블로그 콘텐츠 수집기 | Scrape 기본 |
| 🟢 | 뉴스 헤드라인 모니터링 | Extract 활용 |
| 🟡 | 문서 사이트 RAG 챗봇 | Crawl + LangChain |
| 🟡 | 경쟁사 가격 비교 | 구조화 추출 |
| 🔴 | 전체 사이트 지식베이스 | 대규모 크롤링 |

### 5.2 단계별 구현 가이드: 문서 QA 시스템

**목표**: 공식 문서 사이트를 크롤링하여 QA 시스템 구축

```python
# docs_qa.py
from firecrawl import FirecrawlApp
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os

class DocsQA:
    def __init__(self, firecrawl_key: str, openai_key: str):
        self.app = FirecrawlApp(api_key=firecrawl_key)
        os.environ["OPENAI_API_KEY"] = openai_key
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.vectorstore = None

    def crawl_docs(self, url: str, limit: int = 50):
        """문서 사이트 크롤링"""
        print(f"크롤링 시작: {url}")

        # 먼저 Map으로 확인
        map_result = self.app.map_url(url)
        print(f"발견된 페이지: {len(map_result['links'])}개")

        # 크롤링 실행
        crawl_result = self.app.crawl_url(
            url,
            params={
                "limit": min(limit, len(map_result['links'])),
                "formats": ["markdown"],
                "excludeTags": ["nav", "footer", "sidebar"]
            },
            poll_interval=5
        )

        documents = []
        for page in crawl_result['data']:
            if page.get('markdown'):
                documents.append({
                    'content': page['markdown'],
                    'url': page['metadata']['url'],
                    'title': page['metadata'].get('title', 'Untitled')
                })

        print(f"수집된 문서: {len(documents)}개")
        return documents

    def build_index(self, documents: list):
        """벡터 인덱스 구축"""
        print("인덱스 구축 중...")

        # 청킹
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n## ", "\n### ", "\n\n", "\n", " "]
        )

        all_chunks = []
        for doc in documents:
            chunks = splitter.split_text(doc['content'])
            for chunk in chunks:
                all_chunks.append({
                    'content': chunk,
                    'metadata': {
                        'url': doc['url'],
                        'title': doc['title']
                    }
                })

        # 벡터 스토어 생성
        texts = [c['content'] for c in all_chunks]
        metadatas = [c['metadata'] for c in all_chunks]

        self.vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory="./docs_index"
        )

        print(f"인덱스 완료: {len(all_chunks)}개 청크")

    def ask(self, question: str, k: int = 4) -> str:
        """질문에 답변"""
        if not self.vectorstore:
            return "인덱스가 없습니다. crawl_docs와 build_index를 먼저 실행하세요."

        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})

        prompt = ChatPromptTemplate.from_template("""
        다음 문서 내용을 바탕으로 질문에 답변하세요.
        답변을 찾을 수 없으면 "문서에서 해당 정보를 찾을 수 없습니다"라고 답하세요.

        문서:
        {context}

        질문: {question}

        답변:
        """)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
        )

        response = chain.invoke(question)
        return response.content


# 사용 예시
if __name__ == "__main__":
    qa = DocsQA(
        firecrawl_key="fc-YOUR-KEY",
        openai_key="sk-YOUR-KEY"
    )

    # 문서 크롤링 및 인덱싱
    docs = qa.crawl_docs("https://docs.prefect.io", limit=30)
    qa.build_index(docs)

    # 질문하기
    questions = [
        "Prefect에서 flow를 어떻게 정의하나요?",
        "task에 재시도를 어떻게 설정하나요?",
        "Prefect Cloud와 self-hosted의 차이점은?"
    ]

    for q in questions:
        print(f"\n❓ {q}")
        answer = qa.ask(q)
        print(f"💡 {answer}")
```

### 5.3 Best Practices

**프로젝트 구조**:
```
firecrawl-project/
├── src/
│   ├── crawler.py
│   ├── extractor.py
│   └── qa_system.py
├── data/
│   └── crawled/
├── indexes/
│   └── chroma/
├── config.py
├── requirements.txt
└── README.md
```

**운영 권장사항**:

1. **비용 관리**: Map으로 먼저 확인, 필요한 페이지만 크롤링
2. **캐싱 활용**: 자주 접근하는 페이지는 캐시 활용
3. **에러 처리**: 재시도 로직 구현
4. **증분 크롤링**: 변경된 페이지만 다시 크롤링
5. **로깅**: 모든 API 호출 기록

```python
# 에러 처리 및 재시도
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def safe_scrape(app, url):
    return app.scrape_url(url, params={"formats": ["markdown"]})

# 증분 크롤링
def incremental_crawl(app, url, last_crawl_date):
    map_result = app.map_url(url)

    for page_url in map_result['links']:
        result = app.scrape_url(page_url)
        last_modified = result.get('metadata', {}).get('lastModified')

        if last_modified and last_modified > last_crawl_date:
            # 변경된 페이지만 처리
            process_page(result)
```

---

## 요약

Firecrawl은 RAG 파이프라인을 위한 최고의 웹 데이터 수집 도구입니다:

- **핵심 API**: Scrape (단일), Crawl (전체), Map (URL 목록), Extract (AI 추출)
- **출력**: LLM에 최적화된 Markdown
- **통합**: LangChain, LlamaIndex 네이티브 지원
- **효율성**: 캐싱, 필터링으로 비용 최적화

다음 단계:
1. [무료 계정 생성](https://www.firecrawl.dev/) (500 크레딧)
2. 단일 페이지 Scrape 테스트
3. LangChain으로 RAG 파이프라인 구축
