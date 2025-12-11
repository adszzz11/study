# 구현 마스터 플랜 (Implementation Master Plan)

> 명세를 실제 코드로 구현하는 전체 계획 - 무엇을, 어떻게, 왜 만드는가

## 📋 목차

1. [개요](#개요)
2. [무엇을 만드는가 (What)](#무엇을-만드는가-what)
3. [어떻게 만드는가 (How)](#어떻게-만드는가-how)
4. [왜 이렇게 만드는가 (Why)](#왜-이렇게-만드는가-why)
5. [구현 순서](#구현-순서)
6. [검증 방법](#검증-방법)

---

## 개요

### 목표

Assignment 요구사항 명세를 **실제로 동작하는 코드**로 구현합니다.

**최종 산출물**:
```
✅ 4개 지자체에서 100-400개 문서 수집
✅ SQLite DB + 계층적 파일 구조
✅ LLM 기반 Agentic 시스템
✅ 4가지 제출 문서
```

### 핵심 원칙

1. **Iterative Development**: 작은 단위로 반복
2. **Test-Driven**: 테스트 먼저, 구현 나중
3. **Simplicity First**: 가장 간단한 방법부터
4. **Document Everything**: 모든 결정 문서화

---

## 무엇을 만드는가 (What)

### 1. 핵심 컴포넌트 (7개)

| # | 컴포넌트 | 파일 | 책임 | 라인 수 |
|---|----------|------|------|---------|
| 1 | **Data Models** | `models.py` | 데이터 구조 정의 | ~300 |
| 2 | **Database** | `database.py` | SQLite CRUD | ~400 |
| 3 | **LLM Agent** | `llm_agent.py` | Claude API 통합 | ~250 |
| 4 | **Rule Cache** | `rule_cache.py` | 규칙 저장/로드 | ~80 |
| 5 | **Storage** | `storage.py` | 파일 다운로드/저장 | ~150 |
| 6 | **Base Scraper** | `base_scraper.py` | 추상 인터페이스 | ~100 |
| 7 | **Scrapers** | `cherokee.py` 등 | 지자체별 구현 | ~200 x 4 |

**총 코드**: ~2,000 라인 (주석 포함)

---

### 2. 데이터 구조

#### 2.1 Core Models

```python
# 5개 주요 클래스

class DocumentType(Enum):
    """문서 타입 - 4가지"""
    MINUTES, AGENDA, PACKET, VIDEO

class Jurisdiction(Enum):
    """지자체 - 4곳"""
    CHEROKEE_COUNTY, HOLLY_SPRINGS, ALPHARETTA, MARIETTA

class Document:
    """문서 - 수집 대상"""
    url, title, doc_type, meeting_date, jurisdiction
    file_path, file_size, checksum

class Meeting:
    """회의 - 문서 그룹"""
    date, title, jurisdiction, documents[]

class ScrapingRule:
    """LLM 생성 규칙"""
    jurisdiction, selectors{}, confidence
```

#### 2.2 Database Schema

```sql
-- 3개 테이블

documents (
    id, jurisdiction, doc_type, meeting_date,
    title, source_url, file_path, file_size, checksum,
    scraped_at, metadata
)

scraping_runs (
    id, jurisdiction, run_type, started_at, finished_at,
    status, documents_found, documents_downloaded, errors
)

rules (
    id, jurisdiction, selectors, patterns,
    confidence, created_at, validated
)
```

#### 2.3 File Structure

```
data/
├── documents/
│   ├── cherokee_county/
│   │   └── 2024/
│   │       └── 12/
│   │           └── 2024-12-11_minutes.pdf
│   ├── holly_springs/
│   ├── alpharetta/
│   └── marietta/
├── rules/
│   ├── cherokee_county.json
│   ├── holly_springs.json
│   ├── alpharetta.json
│   └── marietta.json
└── metadata.db
```

---

### 3. API 인터페이스

#### 3.1 BaseScraper (Abstract)

```python
class BaseScraper(ABC):
    # 핵심 메서드 4개

    def get_meeting_list_url() -> str:
        """회의 목록 페이지 URL"""

    def fetch_html(url: str) -> str:
        """HTML 가져오기 (정적/동적)"""

    def parse_meetings(html: str, since: date) -> List[Meeting]:
        """회의 목록 파싱"""

    def parse_documents(meeting: Meeting) -> List[Document]:
        """문서 링크 추출"""

    # 오케스트레이션
    def scrape(since: date) -> List[Document]:
        """전체 프로세스 실행"""
```

#### 3.2 Database

```python
class Database:
    # CRUD 메서드

    def insert_document(doc: Document) -> Optional[int]
    def get_document_by_url(url: str) -> Optional[Document]
    def get_documents(**filters) -> List[Document]
    def get_last_scrape_date(jurisdiction) -> Optional[date]
    def count_documents(**filters) -> int
    def get_statistics() -> dict
```

#### 3.3 LLM Agent

```python
class LLMAgent:
    # 핵심 메서드 1개

    def analyze_page_structure(
        html: str,
        goal: str,
        max_html_length: int = 10000
    ) -> Dict:
        """
        Returns:
        {
            "selectors": {...},
            "date_format": "...",
            "confidence": 0.95,
            "notes": "..."
        }
        """
```

---

## 어떻게 만드는가 (How)

### 1. 개발 방법론

#### TDD (Test-Driven Development)

```
각 컴포넌트마다:

1. 테스트 작성 (RED)
   └─> test_models.py
       test_database.py
       test_llm_agent.py

2. 최소 구현 (GREEN)
   └─> models.py
       database.py
       llm_agent.py

3. 리팩토링 (REFACTOR)
   └─> 코드 개선
       성능 최적화
```

#### Iterative Development

```
Iteration 1: MVP (Week 1)
└─> 1개 지자체 (Cherokee)
    1개 문서 타입 (Minutes)
    10개 이상 문서 수집

Iteration 2: Expand (Week 2)
└─> 4개 지자체 모두
    4개 문서 타입 모두
    Continuous Update

Iteration 3: Polish (Week 3)
└─> 문서화
    테스트 보강
    제출 준비
```

---

### 2. 구현 순서 (Day-by-Day)

#### Week 1: MVP

**Day 1** - 데이터 모델
- [ ] `models.py` 완성
- [ ] 테스트 작성 및 통과
- [ ] Enum, dataclass 검증

**Day 2** - Database
- [ ] `database.py` 완성
- [ ] 스키마 생성
- [ ] CRUD 테스트

**Day 3** - LLM Agent
- [ ] `llm_agent.py` 완성
- [ ] 프롬프트 설계
- [ ] API 호출 테스트

**Day 4** - Rule Cache & Storage
- [ ] `rule_cache.py` 완성
- [ ] `storage.py` 완성
- [ ] 파일 다운로드 테스트

**Day 5** - Base Scraper
- [ ] `base_scraper.py` 추상 클래스
- [ ] 공통 로직 구현

**Day 6** - Cherokee Scraper
- [ ] `cherokee.py` 구현
- [ ] 실제 사이트 테스트
- [ ] 10개 문서 수집 확인

**Day 7** - Integration
- [ ] `main.py` CLI
- [ ] End-to-end 테스트
- [ ] MVP 완성

#### Week 2: Expansion

**Day 8-9** - 추가 지자체
- [ ] Alpharetta (정적)
- [ ] Holly Springs (동적 - Playwright)

**Day 10-11** - Marietta & 문서 타입
- [ ] Marietta (복잡한 구조)
- [ ] Agendas, Packets, Videos 지원

**Day 12-13** - Continuous Update
- [ ] `continuous_mode()` 구현
- [ ] 스케줄러 (`scheduler.py`)
- [ ] 증분 업데이트 테스트

**Day 14** - 통합 테스트
- [ ] 전체 시스템 테스트
- [ ] 성능 측정
- [ ] 비용 측정

#### Week 3: Polish

**Day 15-16** - 문서화
- [ ] README.md
- [ ] SCOPING.md
- [ ] ARCHITECTURE.md
- [ ] QUESTIONS.md

**Day 17** - 최종 테스트
- [ ] 전체 재테스트
- [ ] 코드 정리
- [ ] 린트/타입 체크

**Day 18** - 제출 준비
- [ ] 데모 스크립트
- [ ] 최종 검증
- [ ] 제출

---

### 3. 기술 스택 선택

| 레이어 | 기술 | 왜 선택했나? |
|--------|------|-------------|
| **언어** | Python 3.11+ | - 빠른 프로토타이핑<br>- 풍부한 생태계<br>- Type hints 지원 |
| **웹 스크래핑** | Playwright + BeautifulSoup | - Playwright: 동적 페이지<br>- BS4: 정적 파싱 |
| **HTTP** | httpx | - 비동기 지원<br>- 간결한 API |
| **LLM** | Anthropic Claude 3.5 | - 200K 컨텍스트<br>- 구조화된 출력<br>- 정확도 |
| **DB** | SQLite | - 설치 불필요<br>- 단일 파일<br>- 충분한 성능 |
| **테스트** | pytest | - 표준 프레임워크<br>- Fixture 지원 |
| **타입 체크** | mypy | - 정적 타입 검증 |
| **린트** | ruff | - 빠른 속도<br>- 올인원 |

---

### 4. 설계 패턴

#### 4.1 Plugin Architecture (플러그인)

```python
# 지자체 추가 = 플러그인 추가

class CherokeeScraper(BaseScraper):
    def get_meeting_list_url(self):
        return "http://..."

class AlpharettaScraper(BaseScraper):
    def get_meeting_list_url(self):
        return "http://..."

# 레지스트리
SCRAPERS = {
    'cherokee': CherokeeScraper,
    'alpharetta': AlpharettaScraper,
    # 쉽게 추가 가능
}
```

**장점**:
- 새 지자체 추가 용이
- 코드 재사용
- 독립적 테스트

#### 4.2 Strategy Pattern (전략)

```python
# HTML 가져오기 전략

class StaticFetcher:
    def fetch(url):
        return httpx.get(url).text

class DynamicFetcher:
    def fetch(url):
        # Playwright 사용
        return page.content()

# 지자체에 따라 선택
fetcher = StaticFetcher() if is_static else DynamicFetcher()
```

#### 4.3 Repository Pattern (저장소)

```python
# Database가 Repository 역할

class Database:
    def insert_document(doc)  # Create
    def get_document(id)      # Read
    def update_document(doc)  # Update
    def delete_document(id)   # Delete
```

**장점**:
- 비즈니스 로직과 DB 분리
- 테스트 용이 (Mock 가능)

---

## 왜 이렇게 만드는가 (Why)

### 1. 설계 결정 근거

#### 1.1 Hybrid Agentic (LLM + 규칙)

**대안**:
- Full LLM: 모든 요청마다 LLM
- Full Rule-based: 하드코딩된 규칙만

**선택**: Hybrid

**근거**:
| 항목 | Full LLM | Hybrid | Full Rule |
|------|----------|--------|-----------|
| 비용 | 높음 ($100+) | 낮음 ($10-40) | 없음 |
| 속도 | 느림 | 빠름 | 빠름 |
| 적응성 | 높음 | 중간 | 낮음 |
| 안정성 | 중간 | 높음 | 중간 |

**결론**: Hybrid가 최적의 균형

---

#### 1.2 SQLite (PostgreSQL 대신)

**대안**: PostgreSQL

**선택**: SQLite (MVP), 나중에 PostgreSQL

**근거**:
- **MVP 요구사항**: 10,000개 이하 문서
- **SQLite 한계**: 백만 개까지 충분
- **설치 불필요**: 즉시 시작 가능
- **마이그레이션 용이**: 나중에 PostgreSQL로 쉽게 이동

---

#### 1.3 계층적 파일 구조

**대안**: Flat (모든 파일 한 디렉터리)

**선택**: Hierarchical (`jurisdiction/year/month/`)

**근거**:
```
Flat:
data/documents/
├── 2024-01-15_cherokee_minutes.pdf  # 400개 파일
├── 2024-01-15_alpharetta_minutes.pdf
└── ...

Hierarchical:
data/documents/
├── cherokee_county/
│   └── 2024/
│       └── 01/
│           └── 2024-01-15_minutes.pdf  # 깔끔!
```

**장점**:
- 탐색 용이
- OS 성능 (디렉터리당 파일 수 제한)
- 백업/아카이빙 편리

---

#### 1.4 dataclass (namedtuple 대신)

**대안**: namedtuple, dict, 일반 class

**선택**: dataclass

**근거**:
```python
# namedtuple
Document = namedtuple('Document', ['url', 'title', ...])
# ❌ 타입 체크 없음
# ❌ 메서드 추가 어려움

# dict
doc = {'url': '...', 'title': '...'}
# ❌ 타입 안전성 0
# ❌ IDE 지원 없음

# dataclass
@dataclass
class Document:
    url: str
    title: str
    ...
# ✅ 타입 체크
# ✅ IDE 자동완성
# ✅ 메서드 추가 용이
```

---

### 2. 트레이드오프 분석

| 결정 | 선택 | 장점 | 단점 | 수용 이유 |
|------|------|------|------|-----------|
| **언어** | Python | 빠른 개발 | 느린 속도 | I/O bound 작업이라 속도 무관 |
| **DB** | SQLite | 간단 | 확장성 제한 | MVP는 충분, 나중 마이그레이션 |
| **LLM** | Claude | 정확 | 비용 | Hybrid로 비용 절감 |
| **저장소** | Local | 빠름 | 단일 서버 | MVP는 충분 |

---

## 구현 순서

### Phase 순서 (Why This Order?)

```
Phase 0 → Phase 1 → Phase 2 → Phase 3

왜 이 순서인가?

Phase 0 (조사):
- 구현 전 리스크 제거
- 기술 검증
- MVP 지자체 선정

Phase 1 (MVP):
- 가장 작은 동작하는 시스템
- 조기 피드백
- 아키텍처 검증

Phase 2 (확장):
- 패턴 재사용
- 점진적 복잡도 증가
- 리스크 분산

Phase 3 (완성):
- 문서화에 집중
- 품질 보장
- 제출 준비
```

### 컴포넌트 순서 (Why This Order?)

```
Models → DB → LLM → Storage → Scraper → Main

왜 이 순서인가?

Models:
- 모든 컴포넌트가 의존
- 타입 정의 먼저

DB:
- 데이터 저장 인프라
- 다른 컴포넌트가 사용

LLM:
- Scraper가 사용
- 독립적 테스트 가능

Storage:
- Scraper와 병렬 개발 가능
- 단순함

Scraper:
- 모든 것을 조립
- 비즈니스 로직

Main:
- 최종 통합
- CLI
```

---

## 검증 방법

### 1. Unit Tests (단위 테스트)

**각 컴포넌트**:
```python
# test_models.py
def test_document_creation()
def test_document_type_from_text()
def test_meeting_add_document()

# test_database.py
def test_insert_document()
def test_get_last_scrape_date()
def test_statistics()

# test_llm_agent.py (Mock)
def test_parse_response()
def test_validate_result()
```

**실행**:
```bash
pytest tests/ -v --cov=scraper
```

**목표**: 80% 이상 커버리지

---

### 2. Integration Tests (통합 테스트)

**Mock HTML 사용**:
```python
def test_cherokee_scraper_with_sample_html():
    """실제 사이트 대신 저장된 HTML 사용"""
    html = Path("fixtures/cherokee_sample.html").read_text()

    scraper = CherokeeScraper()
    meetings = scraper.parse_meetings(html)

    assert len(meetings) > 0
    assert all(m.jurisdiction == Jurisdiction.CHEROKEE_COUNTY for m in meetings)
```

**장점**:
- 실제 사이트 부하 없음
- 빠른 실행
- 재현 가능

---

### 3. E2E Tests (종단 간 테스트)

**실제 사이트 사용** (주의):
```python
@pytest.mark.e2e
@pytest.mark.slow
def test_live_cherokee_scraping():
    """실제 사이트에서 스크래핑"""
    scraper = CherokeeScraper()
    docs = scraper.scrape(since=date.today() - timedelta(days=30))

    assert len(docs) > 0
```

**실행**:
```bash
# E2E 테스트는 수동 실행
pytest tests/test_e2e.py -v -m e2e
```

**주의**:
- CI/CD에서 제외
- 주 1회만 실행
- Rate limit 주의

---

### 4. 수동 검증 체크리스트

#### MVP 완성 후
- [ ] `python main.py --dry-run` 성공
- [ ] 10개 이상 문서 발견
- [ ] PDF 다운로드 성공
- [ ] `data/documents/` 파일 구조 확인
- [ ] `data/metadata.db` 쿼리 성공
- [ ] `data/rules/cherokee_county.json` 생성 확인
- [ ] LLM 비용 $15 이하
- [ ] 로그 확인 (에러 없음)

#### Phase 2 완성 후
- [ ] 4개 지자체 모두 동작
- [ ] 4가지 문서 타입 수집
- [ ] Continuous update 테스트
- [ ] 총 100개 이상 문서
- [ ] LLM 비용 $40 이하

#### 제출 전
- [ ] 모든 테스트 통과
- [ ] README 명령어 동작
- [ ] 4가지 제출 문서 완성
- [ ] 데모 스크립트 동작
- [ ] Git 커밋 정리

---

## 요약

### 무엇을 만드는가?
- **7개 컴포넌트** (~2,000 라인)
- **3개 DB 테이블**
- **4개 Scraper** (지자체별)
- **100-400개 문서** 수집

### 어떻게 만드는가?
- **TDD** (테스트 먼저)
- **Iterative** (반복적)
- **Day-by-Day** (단계별)
- **3 Weeks** (21일)

### 왜 이렇게 만드는가?
- **Hybrid Agentic**: 비용 효율
- **Plugin Architecture**: 확장성
- **SQLite**: 간단함
- **Python**: 빠른 개발

---

## 다음 단계

```bash
# 1. 계획 확인
cat implementation-plan/README.md

# 2. 상세 설계 확인
cat implementation-plan/detailed-design.md

# 3. 로드맵 확인
cat implementation-plan/implementation-roadmap.md

# 4. Phase 0 시작
cat implementation-plan/phase-0-research.md
```

---

**작성일**: 2025-12-11
**마지막 업데이트**: 2025-12-11
**상태**: ✅ 계획 완료, 구현 준비 완료
