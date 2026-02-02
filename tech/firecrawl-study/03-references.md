# Firecrawl 참고 자료

## 공식 문서

### 핵심 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| **공식 문서** | [docs.firecrawl.dev](https://docs.firecrawl.dev) | API 레퍼런스, 가이드 |
| **GitHub** | [github.com/mendableai/firecrawl](https://github.com/mendableai/firecrawl) | 소스 코드 (42K+ stars) |
| **대시보드** | [firecrawl.dev/app](https://firecrawl.dev/app) | API 키 관리, 사용량 확인 |
| **Playground** | [firecrawl.dev/playground](https://firecrawl.dev/playground) | 웹에서 직접 테스트 |

### API 문서 구조

```
docs.firecrawl.dev/
├── Introduction
│   ├── Getting Started
│   └── Authentication
├── Features
│   ├── Scrape
│   ├── Crawl
│   ├── Map
│   ├── Extract
│   └── Search
├── Integrations
│   ├── LangChain
│   ├── LlamaIndex
│   └── n8n
└── SDKs
    ├── Python
    ├── Node.js
    └── Go
```

---

## SDK 레포지토리

### Python SDK

```bash
pip install firecrawl-py
```

- **GitHub**: [github.com/mendableai/firecrawl-py](https://github.com/mendableai/firecrawl-py)
- **PyPI**: [pypi.org/project/firecrawl-py](https://pypi.org/project/firecrawl-py)

### Node.js SDK

```bash
npm install @mendable/firecrawl-js
```

- **GitHub**: [github.com/mendableai/firecrawl-js](https://github.com/mendableai/firecrawl-js)
- **npm**: [npmjs.com/package/@mendable/firecrawl-js](https://npmjs.com/package/@mendable/firecrawl-js)

### Go SDK

```bash
go get github.com/mendableai/firecrawl-go
```

- **GitHub**: [github.com/mendableai/firecrawl-go](https://github.com/mendableai/firecrawl-go)

---

## 학습 자료

### 공식 블로그 및 튜토리얼

| 제목 | 내용 |
|------|------|
| [Build a RAG System](https://docs.firecrawl.dev/guides/rag) | RAG 파이프라인 구축 가이드 |
| [LLM Extract Guide](https://docs.firecrawl.dev/guides/llm-extract) | AI 기반 데이터 추출 |
| [Crawl Best Practices](https://docs.firecrawl.dev/guides/crawl-best-practices) | 효율적인 크롤링 전략 |

### YouTube 튜토리얼

- **Firecrawl 공식 채널**: 기본 사용법, 고급 기능
- **AI Jason**: LangChain + Firecrawl 통합
- **프로그래머스**: 한국어 웹 스크래핑 강의

### 추천 학습 순서

```
1. 공식 Getting Started 문서 읽기
   ↓
2. Playground에서 실습
   ↓
3. Python SDK로 간단한 스크래핑
   ↓
4. Crawl API로 사이트 전체 수집
   ↓
5. LangChain 통합 예제 따라하기
   ↓
6. 실전 프로젝트 진행
```

---

## 커뮤니티

### Discord

- **Firecrawl Discord**: [discord.gg/firecrawl](https://discord.gg/gSmWdAkdwd)
- 실시간 질문/답변
- 새 기능 공지
- 사용자 피드백

### GitHub Discussions

- [github.com/mendableai/firecrawl/discussions](https://github.com/mendableai/firecrawl/discussions)
- 기능 제안
- 버그 리포트
- 사용 사례 공유

### 관련 커뮤니티

| 커뮤니티 | 용도 |
|----------|------|
| LangChain Discord | LangChain 통합 관련 |
| r/LocalLLaMA | 로컬 LLM + Firecrawl |
| AI Korea | 한국어 AI 커뮤니티 |

---

## 예제 코드 모음

### 공식 예제

```
github.com/mendableai/firecrawl/
└── examples/
    ├── python/
    │   ├── basic_scrape.py
    │   ├── crawl_website.py
    │   └── langchain_rag.py
    └── node/
        ├── basicScrape.ts
        └── crawlWebsite.ts
```

### 커뮤니티 예제

| 프로젝트 | 설명 | 링크 |
|----------|------|------|
| firecrawl-rag-template | RAG 템플릿 | GitHub |
| web-to-notion | 웹 → Notion 저장 | GitHub |
| competitor-monitor | 경쟁사 모니터링 | GitHub |

---

## API 상태 및 모니터링

### 상태 페이지

- **Status**: [status.firecrawl.dev](https://status.firecrawl.dev)
- 실시간 API 상태 확인
- 인시던트 히스토리

### Rate Limits

```
Free Tier:
- 10 requests/minute
- 500 credits/month

Pro Tier:
- 100 requests/minute
- 3,000 credits/month

Scale Tier:
- Custom limits
- 전용 인프라 옵션
```

---

## 관련 도구 문서

### LangChain 통합

- [LangChain Firecrawl Loader](https://python.langchain.com/docs/integrations/document_loaders/firecrawl)
- [LangChain Web Scraping](https://python.langchain.com/docs/tutorials/web_scraping)

### LlamaIndex 통합

- [LlamaIndex FireCrawlWebReader](https://docs.llamaindex.ai/en/stable/api_reference/readers/web/#llama_index.readers.web.FireCrawlWebReader)

### n8n 통합

- [n8n Firecrawl Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.firecrawl/)

---

## 버전 및 변경 로그

### 최신 버전 확인

```bash
# Python
pip show firecrawl-py

# Node.js
npm view @mendable/firecrawl-js version
```

### 변경 로그

- [GitHub Releases](https://github.com/mendableai/firecrawl/releases)
- [Changelog](https://docs.firecrawl.dev/changelog)

---

## 참고할 만한 블로그 글

### 기술 블로그

| 제목 | 플랫폼 | 주제 |
|------|--------|------|
| Building Production RAG | Medium | RAG 시스템 구축 |
| Web Scraping for AI | Dev.to | AI용 스크래핑 전략 |
| Firecrawl vs Alternatives | Substack | 도구 비교 |

### 한국어 자료

- 네이버 블로그: "Firecrawl로 웹 데이터 수집하기"
- velog: "LangChain + Firecrawl RAG 구현"
- 티스토리: "웹 스크래핑 도구 비교"

---

## 다음 단계

- [[04-learning/01-scrape|Scrape API 실습]] - 첫 번째 스크래핑
- [[04-learning/05-langchain|LangChain 통합]] - RAG 파이프라인 구축
