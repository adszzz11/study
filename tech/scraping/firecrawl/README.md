# Firecrawl 학습 가이드

> 웹사이트를 LLM용 Markdown 및 구조화 데이터로 변환하는 API

## 목차

1. [[01-overview|개요]] - 핵심 개념, 장단점, 사용 사례
2. [[02-ecosystem|에코시스템]] - 관련 기술, 비교, 트렌드
3. [[03-references|참고 자료]] - 공식 문서, 학습 자료, 커뮤니티
4. **Learning Path**
   - [[04-learning/01-scrape|Scrape API]] - 단일 페이지 스크래핑
   - [[04-learning/02-extract|Extract API]] - AI 기반 구조화 데이터 추출
   - [[04-learning/03-crawl|Crawl API]] - 웹사이트 전체 크롤링
   - [[04-learning/04-map|Map API]] - 사이트 URL 목록 수집
   - [[04-learning/05-langchain|LangChain/LlamaIndex 통합]]
   - [[04-learning/06-optimization|캐싱과 비용 최적화]]
5. [[05-projects|실전 프로젝트]] - Best Practices
6. [[cheatsheet|Cheatsheet]] - 빠른 참조

---

## Quick Start

### 설치

```bash
# Python SDK 설치
pip install firecrawl-py

# Node.js SDK 설치
npm install @mendable/firecrawl-js
```

### 기본 사용법

```python
from firecrawl import FirecrawlApp

# API 키로 초기화
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# 단일 페이지 스크래핑
result = app.scrape_url("https://example.com")
print(result["markdown"])
```

### API 키 발급

1. [firecrawl.dev](https://firecrawl.dev) 접속
2. 회원가입 후 대시보드에서 API 키 발급
3. 환경변수로 설정: `export FIRECRAWL_API_KEY=fc-YOUR_API_KEY`

---

## 학습 플랜

### Week 1: 기초 (3-4시간)
- [ ] Firecrawl 개요 및 설치
- [ ] Scrape API로 단일 페이지 변환
- [ ] 결과 포맷 이해 (Markdown, HTML, Links)

### Week 2: 핵심 API (4-5시간)
- [ ] Crawl API로 웹사이트 전체 크롤링
- [ ] Map API로 사이트 구조 파악
- [ ] Extract API로 구조화 데이터 추출

### Week 3: 통합 및 최적화 (4-5시간)
- [ ] LangChain/LlamaIndex 연동
- [ ] 캐싱 전략 및 비용 최적화
- [ ] 에러 핸들링과 재시도 로직

### Week 4: 실전 프로젝트 (5-6시간)
- [ ] 문서 사이트 RAG 파이프라인 구축
- [ ] 경쟁사 모니터링 시스템 구현
- [ ] Production Best Practices 적용

---

## 핵심 특징

| 특징 | 설명 |
|------|------|
| JavaScript 렌더링 | SPA, 동적 콘텐츠 자동 처리 |
| 프록시 및 안티봇 | IP 차단, CAPTCHA 우회 내장 |
| 다양한 출력 포맷 | Markdown, HTML, 스크린샷, 링크 |
| 비동기 크롤링 | 대규모 사이트 효율적 처리 |
| AI 추출 | LLM 기반 구조화 데이터 추출 |

---

## 관련 노트

- [[../web-scraping|웹 스크래핑 기초]]
- [[../langchain|LangChain]]
- [[../rag|RAG 시스템]]
