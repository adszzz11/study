# 실전 프로젝트

## 프로젝트 1: 문서 사이트 RAG 시스템

### 목표
기술 문서 사이트를 크롤링하여 질의응답이 가능한 RAG 시스템 구축

### 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    문서 RAG 시스템                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐          │
│  │ Firecrawl │───▶│ 청킹/처리  │───▶│ ChromaDB  │          │
│  │ Crawler   │    │           │    │           │          │
│  └───────────┘    └───────────┘    └─────┬─────┘          │
│                                          │                │
│  ┌───────────┐    ┌───────────┐    ┌─────▼─────┐          │
│  │ 사용자    │───▶│ 검색+생성  │◀──▶│ GPT-4    │          │
│  │ 질문      │    │           │    │           │          │
│  └───────────┘    └───────────┘    └───────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 구현

```python
# doc_rag_system.py
import os
from datetime import datetime
from firecrawl import FirecrawlApp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class DocumentRAG:
    def __init__(self, firecrawl_key, openai_key, persist_dir="./doc_rag_db"):
        self.app = FirecrawlApp(api_key=firecrawl_key)
        os.environ["OPENAI_API_KEY"] = openai_key
        self.persist_dir = persist_dir
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.vectorstore = None

    def crawl_and_index(self, base_url, limit=100):
        """문서 사이트 크롤링 및 인덱싱"""
        print(f"[1/4] 크롤링 시작: {base_url}")

        result = self.app.crawl_url(base_url, {
            "limit": limit,
            "scrapeOptions": {
                "formats": ["markdown"],
                "onlyMainContent": True,
                "excludeTags": ["nav", "footer", ".sidebar", ".toc"]
            }
        })

        docs = result.get("data", [])
        print(f"[2/4] {len(docs)}개 문서 수집 완료")

        # 청킹
        print("[3/4] 청킹 처리 중...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n## ", "\n### ", "\n\n", "\n", " "]
        )

        all_chunks = []
        for doc in docs:
            chunks = splitter.create_documents(
                texts=[doc["markdown"]],
                metadatas=[{
                    "source": doc["metadata"]["sourceURL"],
                    "title": doc["metadata"].get("title", ""),
                    "indexed_at": datetime.now().isoformat()
                }]
            )
            all_chunks.extend(chunks)

        print(f"[4/4] {len(all_chunks)}개 청크 벡터화 중...")

        # 벡터 저장소 생성
        self.vectorstore = Chroma.from_documents(
            documents=all_chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

        print(f"인덱싱 완료: {len(all_chunks)}개 청크")
        return len(all_chunks)

    def load_existing_index(self):
        """기존 인덱스 로드"""
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )
        print("기존 인덱스 로드 완료")

    def query(self, question, k=5):
        """질문에 답변"""
        if not self.vectorstore:
            raise Exception("인덱스가 로드되지 않았습니다")

        # 프롬프트 템플릿
        prompt_template = """다음 문서 내용을 바탕으로 질문에 답변해주세요.
        답변은 한국어로 해주세요.
        문서에 없는 내용은 "문서에서 해당 정보를 찾을 수 없습니다"라고 답변해주세요.

        문서 내용:
        {context}

        질문: {question}

        답변:"""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # RAG 체인
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": k}),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )

        result = qa_chain.invoke({"query": question})

        return {
            "answer": result["result"],
            "sources": [
                {
                    "url": doc.metadata["source"],
                    "title": doc.metadata.get("title", ""),
                    "content": doc.page_content[:200] + "..."
                }
                for doc in result["source_documents"]
            ]
        }

# 사용 예시
if __name__ == "__main__":
    rag = DocumentRAG(
        firecrawl_key="fc-YOUR_API_KEY",
        openai_key="sk-YOUR_API_KEY"
    )

    # 인덱싱 (최초 1회)
    rag.crawl_and_index("https://docs.langchain.com", limit=50)

    # 또는 기존 인덱스 로드
    # rag.load_existing_index()

    # 질의
    result = rag.query("LangChain에서 에이전트를 만드는 방법은?")
    print(f"답변: {result['answer']}")
    print(f"\n참고 문서:")
    for source in result["sources"]:
        print(f"  - {source['title']}: {source['url']}")
```

---

## 프로젝트 2: 경쟁사 모니터링 시스템

### 목표
경쟁사 웹사이트의 가격, 기능, 뉴스 등을 정기적으로 모니터링하고 변경 시 알림

### 구현

```python
# competitor_monitor.py
import json
import hashlib
from datetime import datetime
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from typing import List, Optional

class PricingInfo(BaseModel):
    plan_name: str
    price: str
    features: List[str]

class CompetitorData(BaseModel):
    company_name: str
    pricing: List[PricingInfo]
    key_features: List[str]
    recent_updates: Optional[List[str]]

class CompetitorMonitor:
    def __init__(self, api_key, data_file="competitor_data.json"):
        self.app = FirecrawlApp(api_key=api_key)
        self.data_file = data_file

    def _load_history(self):
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_history(self, data):
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _content_hash(self, data):
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def monitor_competitor(self, name, pricing_url):
        """경쟁사 가격 페이지 모니터링"""
        print(f"[{name}] 모니터링 중...")

        result = self.app.scrape_url(pricing_url, {
            "formats": ["extract"],
            "extract": {
                "schema": CompetitorData.model_json_schema(),
                "prompt": """이 가격 페이지에서 다음 정보를 추출해주세요:
                - 회사 이름
                - 각 요금제의 이름, 가격, 주요 기능
                - 제품의 핵심 기능들
                - 최근 업데이트나 새 기능이 있다면 포함"""
            }
        })

        current_data = result.get("extract", {})
        current_hash = self._content_hash(current_data)

        # 이전 데이터와 비교
        history = self._load_history()
        previous = history.get(name, {})
        previous_hash = previous.get("hash", "")

        changes = []
        if previous_hash and previous_hash != current_hash:
            changes = self._detect_changes(
                previous.get("data", {}),
                current_data
            )

        # 저장
        history[name] = {
            "url": pricing_url,
            "data": current_data,
            "hash": current_hash,
            "checked_at": datetime.now().isoformat()
        }
        self._save_history(history)

        return {
            "name": name,
            "data": current_data,
            "changes": changes,
            "is_new": not previous_hash
        }

    def _detect_changes(self, old_data, new_data):
        """변경 사항 감지"""
        changes = []

        # 가격 변경 확인
        old_pricing = {p.get("plan_name"): p for p in old_data.get("pricing", [])}
        new_pricing = {p.get("plan_name"): p for p in new_data.get("pricing", [])}

        for plan, info in new_pricing.items():
            if plan not in old_pricing:
                changes.append(f"새 요금제 추가: {plan}")
            elif old_pricing[plan].get("price") != info.get("price"):
                changes.append(
                    f"가격 변경: {plan} "
                    f"({old_pricing[plan].get('price')} → {info.get('price')})"
                )

        # 기능 변경 확인
        old_features = set(old_data.get("key_features", []))
        new_features = set(new_data.get("key_features", []))

        added = new_features - old_features
        removed = old_features - new_features

        for feature in added:
            changes.append(f"새 기능 추가: {feature}")
        for feature in removed:
            changes.append(f"기능 제거: {feature}")

        return changes

    def run_monitoring(self, competitors):
        """전체 경쟁사 모니터링 실행"""
        results = []

        for competitor in competitors:
            result = self.monitor_competitor(
                competitor["name"],
                competitor["url"]
            )
            results.append(result)

            if result["changes"]:
                self._send_alert(competitor["name"], result["changes"])

        return results

    def _send_alert(self, name, changes):
        """알림 전송 (Slack, Email 등)"""
        print(f"\n🚨 [{name}] 변경 감지!")
        for change in changes:
            print(f"  - {change}")
        # 실제로는 Slack webhook, Email 등으로 전송

# 사용 예시
if __name__ == "__main__":
    monitor = CompetitorMonitor(api_key="fc-YOUR_API_KEY")

    competitors = [
        {"name": "Competitor A", "url": "https://competitor-a.com/pricing"},
        {"name": "Competitor B", "url": "https://competitor-b.com/pricing"},
    ]

    results = monitor.run_monitoring(competitors)

    print("\n=== 모니터링 결과 ===")
    for result in results:
        print(f"\n{result['name']}:")
        if result["is_new"]:
            print("  (첫 수집)")
        elif result["changes"]:
            print(f"  변경: {len(result['changes'])}건")
        else:
            print("  변경 없음")
```

---

## 프로젝트 3: 콘텐츠 수집 자동화

### 목표
특정 주제의 블로그/뉴스 콘텐츠를 수집하여 요약 및 저장

### 구현

```python
# content_collector.py
import json
from datetime import datetime
from firecrawl import FirecrawlApp
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class ContentCollector:
    def __init__(self, firecrawl_key, openai_key):
        self.app = FirecrawlApp(api_key=firecrawl_key)
        self.llm = ChatOpenAI(api_key=openai_key, model="gpt-4")

    def collect_from_sources(self, sources, limit_per_source=10):
        """여러 소스에서 콘텐츠 수집"""
        all_content = []

        for source in sources:
            print(f"수집 중: {source['name']}")

            result = self.app.crawl_url(source["url"], {
                "limit": limit_per_source,
                "includePaths": source.get("paths", []),
                "scrapeOptions": {
                    "formats": ["markdown"],
                    "onlyMainContent": True
                }
            })

            for page in result.get("data", []):
                all_content.append({
                    "source": source["name"],
                    "url": page["metadata"]["sourceURL"],
                    "title": page["metadata"].get("title", ""),
                    "content": page["markdown"],
                    "collected_at": datetime.now().isoformat()
                })

        return all_content

    def summarize_content(self, content):
        """콘텐츠 요약"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 기술 콘텐츠를 요약하는 전문가입니다."),
            ("user", """다음 글을 3-5문장으로 요약해주세요.
            핵심 포인트와 주요 인사이트를 포함해주세요.

            제목: {title}
            내용: {content}

            요약:""")
        ])

        chain = prompt | self.llm

        summaries = []
        for item in content:
            try:
                result = chain.invoke({
                    "title": item["title"],
                    "content": item["content"][:3000]  # 토큰 제한
                })
                summaries.append({
                    **item,
                    "summary": result.content
                })
            except Exception as e:
                print(f"요약 실패: {item['title']} - {e}")

        return summaries

    def generate_digest(self, summaries, topic):
        """뉴스레터/다이제스트 생성"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 기술 뉴스레터 작성 전문가입니다."),
            ("user", """다음 콘텐츠 요약들을 바탕으로 '{topic}' 주제의 주간 다이제스트를 작성해주세요.

            콘텐츠:
            {content}

            다이제스트 형식:
            1. 이번 주 하이라이트 (1-2문장)
            2. 주요 트렌드 (3-5개 불릿포인트)
            3. 추천 읽을거리 (상위 3개)
            4. 한 줄 인사이트

            다이제스트:""")
        ])

        content_text = "\n\n".join([
            f"제목: {s['title']}\n출처: {s['source']}\n요약: {s['summary']}"
            for s in summaries
        ])

        chain = prompt | self.llm
        result = chain.invoke({"topic": topic, "content": content_text})

        return result.content

    def save_results(self, summaries, digest, output_dir="./collected"):
        """결과 저장"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 상세 데이터 저장
        with open(f"{output_dir}/content_{timestamp}.json", "w") as f:
            json.dump(summaries, f, indent=2, ensure_ascii=False)

        # 다이제스트 저장
        with open(f"{output_dir}/digest_{timestamp}.md", "w") as f:
            f.write(f"# 콘텐츠 다이제스트\n\n")
            f.write(f"생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(digest)

        print(f"저장 완료: {output_dir}")

# 사용 예시
if __name__ == "__main__":
    collector = ContentCollector(
        firecrawl_key="fc-YOUR_API_KEY",
        openai_key="sk-YOUR_API_KEY"
    )

    # 소스 정의
    sources = [
        {
            "name": "AI News",
            "url": "https://ai-news-site.com",
            "paths": ["/blog/*", "/news/*"]
        },
        {
            "name": "Tech Blog",
            "url": "https://tech-blog.com",
            "paths": ["/posts/*"]
        }
    ]

    # 수집
    content = collector.collect_from_sources(sources, limit_per_source=10)
    print(f"총 {len(content)}개 콘텐츠 수집")

    # 요약
    summaries = collector.summarize_content(content)

    # 다이제스트 생성
    digest = collector.generate_digest(summaries, "AI/ML 트렌드")

    # 저장
    collector.save_results(summaries, digest)
```

---

## Best Practices

### 1. 에러 처리와 재시도

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    """지수 백오프를 사용한 재시도 데코레이터"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    print(f"재시도 {attempt + 1}/{max_retries}, {delay}초 후...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def safe_scrape(app, url, options=None):
    return app.scrape_url(url, options or {})
```

### 2. 로깅과 모니터링

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("firecrawl")

def logged_scrape(app, url, options=None):
    logger.info(f"스크래핑 시작: {url}")
    start = time.time()

    try:
        result = app.scrape_url(url, options or {})
        elapsed = time.time() - start
        logger.info(f"스크래핑 완료: {url} ({elapsed:.2f}s)")
        return result
    except Exception as e:
        logger.error(f"스크래핑 실패: {url} - {e}")
        raise
```

### 3. 설정 관리

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    firecrawl_api_key: str
    openai_api_key: str
    cache_ttl_hours: int = 24
    max_pages_per_crawl: int = 100
    rate_limit_per_minute: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
```

### 4. 테스트 전략

```python
# test_firecrawl.py
import pytest
from unittest.mock import Mock, patch

def test_scrape_returns_markdown():
    """스크래핑 결과에 마크다운이 포함되는지 테스트"""
    mock_result = {
        "success": True,
        "markdown": "# Test\n\nContent",
        "metadata": {"title": "Test"}
    }

    with patch.object(FirecrawlApp, 'scrape_url', return_value=mock_result):
        app = FirecrawlApp(api_key="test")
        result = app.scrape_url("https://example.com")

        assert "markdown" in result
        assert result["markdown"].startswith("#")
```

---

## 다음 단계

- [[cheatsheet|Cheatsheet]] - 빠른 참조
- [[04-learning/06-optimization|캐싱과 비용 최적화]]
