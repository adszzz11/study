# Phase 4 계획 (선택적 기능)

> **상태**: 계획 단계
> **우선순위**: 선택적 (Phase 0-3 완료 후)
> **예상 시간**: 2-3주

---

## 📌 Executive Summary

Phase 0-3에서 4개 지자체의 기본 스크래핑 기능이 완성되었습니다. Phase 4에서는 프로덕션 환경을 위한 고급 기능들을 추가합니다.

**Phase 4 목표**:
- Continuous 모드 (실시간 업데이트)
- 문서 다운로드 및 저장
- LLM 통합 (Agentic 기능)
- 프로덕션 인프라

---

## 🎯 Phase 4 기능

### 1. Continuous 모드 (1-2일)

**목표**: 새로운 문서만 증분 수집

**현재 한계**:
- Backfill 모드만 지원 (전체 수집)
- 중복 검사는 있지만 전체 페이지 파싱 필요
- 스케줄링 기능 없음

**구현 사항**:

1. **증분 업데이트 로직**
   ```python
   # src/scrapers/base.py
   class BaseScraper:
       def scrape_since(self, since_date: date) -> DocumentList:
           """특정 날짜 이후 문서만 수집"""
           pass

       def scrape_new(self) -> DocumentList:
           """마지막 수집 이후 새 문서만"""
           last_date = self.db.get_last_scrape_date(self.JURISDICTION)
           return self.scrape_since(last_date)
   ```

2. **스케줄러 통합**
   ```python
   # src/scheduler.py
   from apscheduler.schedulers.blocking import BlockingScheduler

   def scheduled_scrape(jurisdiction: str):
       """정기 실행"""
       scraper = get_scraper(jurisdiction)
       documents = scraper.scrape_new()
       db.insert_many(documents)

   scheduler = BlockingScheduler()
   scheduler.add_job(scheduled_scrape, 'cron', hour=6)  # 매일 오전 6시
   ```

3. **알림 시스템**
   ```python
   # src/notifications.py
   def notify_new_documents(documents: DocumentList):
       """새 문서 발견 시 알림"""
       # Email
       send_email(f"Found {len(documents)} new documents")

       # Slack
       send_slack_message(f"🔔 New documents: {len(documents)}")
   ```

4. **CLI 명령어**
   ```bash
   # Continuous 모드 실행
   python -m src.main continuous --jurisdiction cherokee

   # 특정 날짜 이후 수집
   python -m src.main incremental --jurisdiction marietta --since 2025-01-01

   # 모든 지자체 스케줄러 실행
   python -m src.main scheduler --config scheduler.yaml
   ```

**예상 시간**: 1-2일
**우선순위**: 🟡 중간

---

### 2. 문서 다운로드 기능 (1일)

**목표**: PDF/문서 파일을 로컬에 저장

**현재 한계**:
- URL만 저장 (외부 링크 의존)
- 파일 유실 위험
- 오프라인 접근 불가

**구현 사항**:

1. **다운로드 매니저**
   ```python
   # src/downloader.py
   class DocumentDownloader:
       def download(self, doc: Document) -> Path:
           """문서 다운로드 및 저장"""
           response = httpx.get(doc.url)

           # 파일명 생성
           filename = f"{doc.jurisdiction.value}_{doc.doc_type.value}_{doc.meeting_date}_{doc.id}.pdf"
           file_path = config.DOWNLOAD_DIR / filename

           # 저장
           file_path.write_bytes(response.content)

           # 체크섬 계산
           checksum = hashlib.sha256(response.content).hexdigest()

           return file_path, checksum
   ```

2. **중복 방지**
   ```python
   def download_if_needed(doc: Document) -> Optional[Path]:
       """이미 다운로드된 경우 스킵"""
       if doc.file_path and doc.file_path.exists():
           # 체크섬 검증
           current_checksum = calculate_checksum(doc.file_path)
           if current_checksum == doc.checksum:
               return None  # 이미 존재

       return download(doc)
   ```

3. **스토리지 구조**
   ```
   data/downloads/
   ├── cherokee/
   │   ├── 2025/
   │   │   ├── 01/
   │   │   │   ├── agenda_2025-01-15_123.pdf
   │   │   │   └── minutes_2025-01-15_124.pdf
   ```

4. **CLI 명령어**
   ```bash
   # 모든 문서 다운로드
   python -m src.main download --all

   # 특정 지자체만
   python -m src.main download --jurisdiction cherokee

   # 특정 기간
   python -m src.main download --since 2025-01-01
   ```

**예상 시간**: 1일
**우선순위**: 🟡 중간

---

### 3. LLM 통합 (2-3일)

**목표**: Agentic 기능으로 자동화 및 지능화

**활용 사례**:

#### 3.1. CSS Selector 자동 추출

**문제**: 새 지자체 추가 시 HTML 분석 필요

**해결책**:
```python
# src/llm/selector_extractor.py
from anthropic import Anthropic

class SelectorExtractor:
    def extract_selectors(self, html: str, platform: str) -> dict:
        """LLM에게 HTML에서 CSS Selector 추출 요청"""

        prompt = f"""
        다음은 {platform} 플랫폼의 HTML입니다.

        회의 목록, 회의 날짜, 회의 제목, 문서 링크를 추출하기 위한
        CSS Selector를 찾아주세요.

        HTML:
        {html[:5000]}

        JSON 형식으로 응답:
        {{
            "meeting_container": "...",
            "meeting_items": "...",
            "meeting_date": "...",
            "meeting_title": "...",
            "document_links": "..."
        }}
        """

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)
```

**CLI**:
```bash
# 새 지자체의 Selector 자동 추출
python -m src.main llm extract-selectors --url https://newcity.gov/meetings
```

#### 3.2. 에러 자동 복구

**문제**: HTML 구조 변경 시 스크래퍼 실패

**해결책**:
```python
# src/llm/error_recovery.py
class ErrorRecovery:
    def recover_from_parsing_error(self, html: str, error: Exception) -> dict:
        """파싱 실패 시 LLM에게 새 전략 요청"""

        prompt = f"""
        HTML 파싱 중 에러가 발생했습니다.

        에러: {error}
        HTML: {html[:3000]}

        문제를 분석하고 새로운 CSS Selector를 제안해주세요.
        """

        # LLM 호출
        new_selectors = self.client.messages.create(...)

        return new_selectors
```

#### 3.3. 문서 내용 분석

**목표**: 문서 내용을 요약하고 분류

```python
# src/llm/document_analyzer.py
class DocumentAnalyzer:
    def analyze_document(self, doc_path: Path) -> dict:
        """문서 내용 분석"""

        # PDF 텍스트 추출
        text = extract_text_from_pdf(doc_path)

        prompt = f"""
        다음은 Planning & Zoning 회의 문서입니다.

        1. 주요 안건 요약
        2. 결정 사항
        3. 이해관계자
        4. 중요도 평가

        문서:
        {text[:10000]}
        """

        analysis = self.client.messages.create(...)

        return {
            "summary": "...",
            "decisions": [...],
            "stakeholders": [...],
            "importance": "high/medium/low"
        }
```

**CLI**:
```bash
# 문서 분석
python -m src.main llm analyze --document-id 123

# 모든 신규 문서 분석
python -m src.main llm analyze-new
```

**예상 시간**: 2-3일
**우선순위**: 🟢 낮음 (고급 기능)

---

### 4. PostgreSQL 마이그레이션 (1일)

**목표**: 프로덕션 데이터베이스로 전환

**현재 한계**:
- SQLite는 단일 파일 (백업 어려움)
- 동시 쓰기 제한
- 확장성 부족

**구현 사항**:

1. **마이그레이션 스크립트**
   ```python
   # scripts/migrate_to_postgres.py
   import psycopg2

   def migrate():
       # SQLite에서 데이터 읽기
       sqlite_db = Database("documents.db")
       documents = sqlite_db.get_all_documents()

       # PostgreSQL에 쓰기
       pg_conn = psycopg2.connect(
           host="localhost",
           database="zonagent",
           user="zonagent",
           password="..."
       )

       for doc in documents:
           pg_conn.execute(
               "INSERT INTO documents (...) VALUES (...)",
               doc.to_tuple()
           )
   ```

2. **데이터베이스 추상화**
   ```python
   # src/database.py
   class Database:
       def __init__(self, backend: str = "sqlite"):
           if backend == "sqlite":
               self.conn = sqlite3.connect(...)
           elif backend == "postgresql":
               self.conn = psycopg2.connect(...)
   ```

3. **설정**
   ```yaml
   # config.yaml
   database:
     backend: postgresql
     host: localhost
     port: 5432
     database: zonagent
     user: zonagent
   ```

**예상 시간**: 1일
**우선순위**: 🟡 중간

---

### 5. Docker 컨테이너화 (1일)

**목표**: 배포 간소화

**구현 사항**:

1. **Dockerfile**
   ```dockerfile
   # Dockerfile
   FROM python:3.11-slim

   # Playwright 브라우저 설치
   RUN apt-get update && apt-get install -y \
       chromium \
       && rm -rf /var/lib/apt/lists/*

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt
   RUN playwright install chromium

   COPY src/ ./src/

   CMD ["python", "-m", "src.main", "scheduler"]
   ```

2. **docker-compose.yml**
   ```yaml
   version: '3.8'

   services:
     zonagent:
       build: .
       volumes:
         - ./data:/app/data
       environment:
         - DATABASE_URL=postgresql://postgres:5432/zonagent
       depends_on:
         - postgres

     postgres:
       image: postgres:15
       environment:
         POSTGRES_DB: zonagent
         POSTGRES_USER: zonagent
         POSTGRES_PASSWORD: secret
       volumes:
         - postgres_data:/var/lib/postgresql/data

   volumes:
     postgres_data:
   ```

3. **실행**
   ```bash
   # 빌드 및 실행
   docker-compose up -d

   # 로그 확인
   docker-compose logs -f zonagent

   # 수동 실행
   docker-compose exec zonagent python -m src.main backfill -j cherokee
   ```

**예상 시간**: 1일
**우선순위**: 🟢 낮음

---

### 6. CI/CD 파이프라인 (1일)

**목표**: 자동 테스트 및 배포

**구현 사항**:

1. **GitHub Actions**
   ```yaml
   # .github/workflows/test.yml
   name: Test

   on: [push, pull_request]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             pip install -r requirements.txt
             playwright install chromium

         - name: Run tests
           run: pytest tests/

         - name: Lint
           run: |
             flake8 src/
             mypy src/
   ```

2. **단위 테스트**
   ```python
   # tests/test_scrapers.py
   import pytest
   from src.scrapers import CherokeeScraper

   def test_cherokee_scraper():
       scraper = CherokeeScraper()
       documents = scraper.scrape(limit=5)

       assert len(documents) > 0
       assert all(doc.jurisdiction == Jurisdiction.CHEROKEE for doc in documents)
   ```

**예상 시간**: 1일
**우선순위**: 🟡 중간

---

### 7. 모니터링 및 로깅 (1일)

**목표**: 운영 가시성 확보

**구현 사항**:

1. **구조화된 로깅**
   ```python
   # src/logging_config.py
   import structlog

   logger = structlog.get_logger()

   logger.info(
       "document_scraped",
       jurisdiction="cherokee",
       doc_type="agenda",
       meeting_date="2025-01-15",
       duration_ms=1234
   )
   ```

2. **메트릭 수집**
   ```python
   # src/metrics.py
   from prometheus_client import Counter, Histogram

   documents_scraped = Counter(
       'documents_scraped_total',
       'Total documents scraped',
       ['jurisdiction', 'doc_type']
   )

   scrape_duration = Histogram(
       'scrape_duration_seconds',
       'Time to scrape',
       ['jurisdiction']
   )
   ```

3. **대시보드**
   - Grafana 대시보드
   - 수집 현황 시각화
   - 에러율 추적

**예상 시간**: 1일
**우선순위**: 🟢 낮음

---

## 📊 Phase 4 로드맵

### Week 1: 핵심 기능

| 일 | 작업 | 시간 |
|----|------|------|
| Mon | Continuous 모드 설계 및 구현 | 8h |
| Tue | 스케줄러 및 알림 시스템 | 8h |
| Wed | 문서 다운로드 기능 | 8h |
| Thu | 테스트 및 통합 | 4h |
| Thu | PostgreSQL 마이그레이션 | 4h |
| Fri | Docker 컨테이너화 | 8h |

**Week 1 총계**: 40시간

### Week 2: LLM 통합 (선택)

| 일 | 작업 | 시간 |
|----|------|------|
| Mon | CSS Selector 자동 추출 | 8h |
| Tue | 에러 자동 복구 | 8h |
| Wed | 문서 내용 분석 | 8h |
| Thu | 테스트 및 통합 | 8h |
| Fri | 문서화 | 8h |

**Week 2 총계**: 40시간

### Week 3: 운영 인프라 (선택)

| 일 | 작업 | 시간 |
|----|------|------|
| Mon | CI/CD 파이프라인 | 8h |
| Tue | 모니터링 및 로깅 | 8h |
| Wed | 통합 테스트 | 8h |
| Thu | 프로덕션 배포 | 8h |
| Fri | 최종 문서화 | 8h |

**Week 3 총계**: 40시간

---

## 🎯 우선순위

### Must Have (필수)

1. ✅ **Continuous 모드** - 실용성 핵심
2. ✅ **문서 다운로드** - 데이터 안정성

**예상 시간**: 2-3일

### Should Have (권장)

3. 🟡 **PostgreSQL** - 확장성
4. 🟡 **Docker** - 배포 편의성
5. 🟡 **CI/CD** - 자동화

**예상 시간**: +3일 (총 5-6일)

### Nice to Have (선택)

6. 🟢 **LLM 통합** - 고급 기능
7. 🟢 **모니터링** - 운영 편의성

**예상 시간**: +3일 (총 8-9일)

---

## 💰 예상 비용

### 인프라

| 항목 | 비용/월 |
|------|---------|
| PostgreSQL (AWS RDS) | $15-50 |
| Docker 호스팅 (AWS ECS) | $20-100 |
| LLM API (Claude) | $10-50 (사용량 기반) |
| 모니터링 (Grafana Cloud) | $0-29 |
| **총계** | **$45-229/월** |

### 개발 시간

| Phase | 시간 | 비용 (시급 $100) |
|-------|------|------------------|
| Must Have | 20-24h | $2,000-2,400 |
| Should Have | +24h | +$2,400 |
| Nice to Have | +24h | +$2,400 |
| **총계** | 68-72h | $6,800-7,200 |

---

## ✅ 체크리스트

### Phase 4.1: Continuous (필수)

- [ ] 증분 업데이트 로직
- [ ] 스케줄러 통합 (APScheduler)
- [ ] 이메일 알림
- [ ] Slack 알림 (선택)
- [ ] CLI 명령어
- [ ] 테스트
- [ ] 문서화

### Phase 4.2: 문서 다운로드 (필수)

- [ ] 다운로드 매니저
- [ ] 체크섬 검증
- [ ] 중복 방지
- [ ] 스토리지 구조
- [ ] CLI 명령어
- [ ] 테스트
- [ ] 문서화

### Phase 4.3: PostgreSQL (권장)

- [ ] 마이그레이션 스크립트
- [ ] 데이터베이스 추상화
- [ ] 설정 시스템
- [ ] 테스트
- [ ] 문서화

### Phase 4.4: Docker (권장)

- [ ] Dockerfile
- [ ] docker-compose.yml
- [ ] 빌드 테스트
- [ ] 문서화

### Phase 4.5: LLM (선택)

- [ ] CSS Selector 자동 추출
- [ ] 에러 자동 복구
- [ ] 문서 분석
- [ ] API 키 관리
- [ ] 비용 모니터링
- [ ] 테스트
- [ ] 문서화

---

## 🎉 Phase 4 완료 시

**달성 목표**:
- ✅ 완전 자동화된 실시간 수집
- ✅ 안정적인 데이터 저장
- ✅ 프로덕션 준비 완료
- ✅ (선택) Agentic AI 기능

**프로젝트 상태**: 🚀 **프로덕션 준비 완료**

---

**작성일**: 2025-12-12
**Phase**: 4 (선택적 기능)
**상태**: 계획 단계
**의존성**: Phase 0-3 완료 필수
