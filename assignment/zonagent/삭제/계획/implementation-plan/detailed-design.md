# 상세 구현 설계 (Detailed Implementation Design)

> 명세를 실제 코드로 구현하기 위한 구체적인 설계 문서

## 📋 개요

이 문서는 Zonagent 과제의 요구사항 명세를 **실제로 어떻게 구현할 것인지** 구체적으로 설계합니다.

**핵심 질문**:
- 무엇을 만들 것인가? (What)
- 어떻게 만들 것인가? (How)
- 왜 이렇게 만드는가? (Why)

---

## 🎯 구현 목표

### 최종 산출물

```
zonagent-scraper/
├── 동작하는 코드      ✅ 4개 지자체에서 문서 수집
├── 데이터             ✅ 100-400개 PDF + 메타데이터 DB
├── 문서               ✅ README, 3개 제출 문서
└── 데모               ✅ 실행 가능한 시연
```

### 핵심 요구사항 구현

| 요구사항 | 구현 방법 | 검증 방법 |
|---------|----------|----------|
| **4개 지자체** | 4개 Scraper 클래스 | 각각 10개 이상 문서 수집 |
| **4가지 문서 타입** | DocumentType Enum + 분류 로직 | 타입별 카운트 확인 |
| **Agentic** | LLM + 규칙 캐싱 | LLM 호출 로그 확인 |
| **Backfill** | since 파라미터 | 날짜 필터링 검증 |
| **Continuous** | last_scrape_date 추적 | 증분 업데이트 테스트 |

---

## 🏗️ 시스템 아키텍처

### 1. 레이어 구조

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│                  (CLI, Scheduler, Demo)                  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────┐
│                  Application Layer                       │
│         (Orchestration, Workflow Control)                │
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Backfill    │  │ Continuous  │  │  Validator  │     │
│  │ Controller  │  │ Controller  │  │             │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────┐
│                   Domain Layer                           │
│              (Business Logic, Scrapers)                  │
│                                                           │
│  ┌─────────────────────────────────────────────┐        │
│  │          BaseScraper (Abstract)              │        │
│  │  - scrape()                                  │        │
│  │  - fetch_html()                              │        │
│  │  - parse_meetings()                          │        │
│  │  - parse_documents()                         │        │
│  └────────┬────────────────────────────────────┘        │
│           │                                              │
│  ┌────────┴────────┬──────────────┬──────────────┐     │
│  │                 │              │              │     │
│  ▼                 ▼              ▼              ▼     │
│  Cherokee      Holly Springs  Alpharetta    Marietta   │
│  Scraper          Scraper       Scraper      Scraper   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────┐
│                Infrastructure Layer                      │
│         (Storage, Database, External APIs)               │
│                                                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │   LLM   │  │  Rule   │  │ Storage │  │Database │   │
│  │  Agent  │  │  Cache  │  │ Manager │  │   (DB)  │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 2. 데이터 흐름

```
사용자 요청
    ↓
CLI (main.py)
    ↓
Controller (Backfill/Continuous)
    ↓
┌──────────────────────────────────────┐
│   Scraper (예: CherokeeScraper)      │
│                                      │
│   1. fetch_html(url)                 │
│      ↓                               │
│   2. ensure_rules(html)              │
│      ├─→ RuleCache.load()            │
│      └─→ LLM.analyze() (if needed)   │
│      ↓                               │
│   3. parse_meetings(html)            │
│      ↓                               │
│   4. parse_documents(meeting)        │
│      ↓                               │
│   5. return List[Document]           │
└──────────────────────────────────────┘
    ↓
Storage.download_document(doc)
    ↓
Database.insert_document(doc)
    ↓
결과 반환 (성공/실패 통계)
```

---

## 🔧 컴포넌트 상세 설계

### Component 1: Data Models

**파일**: `scraper/models.py`

**무엇을 만드는가?**
- 시스템 전체에서 사용할 데이터 구조 정의

**어떻게 만드는가?**

```python
# 설계 원칙:
# 1. Immutability: dataclass + frozen
# 2. Type Safety: 모든 필드에 타입 명시
# 3. Validation: __post_init__ 활용

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum
import hashlib

# ===== Enums (타입 안전성) =====

class DocumentType(Enum):
    """문서 타입 - 4가지 고정"""
    MINUTES = "minutes"
    AGENDA = "agenda"
    PACKET = "packet"
    VIDEO = "video"

    @classmethod
    def from_text(cls, text: str) -> 'DocumentType':
        """텍스트에서 문서 타입 추론"""
        text_lower = text.lower()
        if 'minute' in text_lower:
            return cls.MINUTES
        elif 'agenda' in text_lower:
            if 'packet' in text_lower:
                return cls.PACKET
            return cls.AGENDA
        elif 'packet' in text_lower:
            return cls.PACKET
        elif 'video' in text_lower or 'recording' in text_lower:
            return cls.VIDEO
        else:
            # 기본값
            return cls.MINUTES

class Jurisdiction(Enum):
    """지자체 - 4곳 고정"""
    CHEROKEE_COUNTY = "cherokee_county"
    HOLLY_SPRINGS = "holly_springs"
    ALPHARETTA = "alpharetta"
    MARIETTA = "marietta"

    @property
    def display_name(self) -> str:
        """사람이 읽기 쉬운 이름"""
        names = {
            self.CHEROKEE_COUNTY: "Cherokee County",
            self.HOLLY_SPRINGS: "City of Holly Springs",
            self.ALPHARETTA: "City of Alpharetta",
            self.MARIETTA: "City of Marietta"
        }
        return names[self]

# ===== Core Models =====

@dataclass
class Document:
    """
    문서 정보

    설계 결정:
    - url: 소스 URL (UNIQUE 제약조건)
    - file_path: 다운로드 후 채워짐
    - checksum: 중복 방지용 SHA256
    """
    url: str
    title: str
    doc_type: DocumentType
    meeting_date: date
    jurisdiction: Jurisdiction

    # Optional fields (다운로드 후 채워짐)
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    checksum: Optional[str] = None
    scraped_at: Optional[datetime] = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """유효성 검증"""
        # Enum 자동 변환
        if isinstance(self.doc_type, str):
            self.doc_type = DocumentType(self.doc_type)
        if isinstance(self.jurisdiction, str):
            self.jurisdiction = Jurisdiction(self.jurisdiction)

        # URL 유효성
        if not self.url.startswith('http'):
            raise ValueError(f"Invalid URL: {self.url}")

        # 날짜 유효성
        if self.meeting_date > date.today():
            raise ValueError(f"Meeting date cannot be in the future: {self.meeting_date}")

    def calculate_checksum(self, content: bytes) -> str:
        """문서 내용의 체크섬 계산"""
        self.checksum = hashlib.sha256(content).hexdigest()
        return self.checksum

    @property
    def filename(self) -> str:
        """권장 파일명 생성"""
        # 예: 2024-12-11_minutes.pdf
        return f"{self.meeting_date.isoformat()}_{self.doc_type.value}.pdf"


@dataclass
class Meeting:
    """
    회의 정보

    설계 결정:
    - documents는 빈 리스트로 시작
    - url은 회의 상세 페이지 (또는 목록 페이지)
    """
    date: date
    title: str
    jurisdiction: Jurisdiction
    url: str
    documents: List[Document] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_document(self, doc: Document):
        """문서 추가 (타입 검증)"""
        if not isinstance(doc, Document):
            raise TypeError("Must be a Document instance")
        if doc.jurisdiction != self.jurisdiction:
            raise ValueError("Document jurisdiction mismatch")
        if doc.meeting_date != self.date:
            raise ValueError("Document date mismatch")
        self.documents.append(doc)


@dataclass
class ScrapingRule:
    """
    LLM이 생성한 스크래핑 규칙

    설계 결정:
    - selectors: CSS selectors dict
    - patterns: 정규식 패턴 (날짜 등)
    - confidence: LLM의 확신도 (0.0-1.0)
    - validated: 실제 동작 검증 여부
    """
    jurisdiction: Jurisdiction
    selectors: dict
    confidence: float
    created_at: datetime = field(default_factory=datetime.now)
    patterns: Optional[dict] = None
    validated: bool = False
    validation_count: int = 0  # 성공 횟수
    failure_count: int = 0     # 실패 횟수

    def __post_init__(self):
        """유효성 검증"""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0 and 1")

        # 필수 selector 확인
        required = ['meeting_rows', 'date']
        for key in required:
            if key not in self.selectors:
                raise ValueError(f"Missing required selector: {key}")

    @property
    def is_reliable(self) -> bool:
        """규칙이 신뢰할 수 있는가?"""
        # 10회 이상 성공, 실패율 10% 이하
        if self.validation_count < 10:
            return False
        failure_rate = self.failure_count / (self.validation_count + self.failure_count)
        return failure_rate < 0.1

    def mark_success(self):
        """성공 기록"""
        self.validation_count += 1
        self.validated = True

    def mark_failure(self):
        """실패 기록"""
        self.failure_count += 1


@dataclass
class ScrapingRun:
    """
    스크래핑 실행 정보 (메타데이터)

    설계 결정:
    - 각 실행마다 기록 (디버깅, 모니터링용)
    """
    jurisdiction: Jurisdiction
    run_type: str  # 'backfill' or 'continuous'
    started_at: datetime = field(default_factory=datetime.now)
    finished_at: Optional[datetime] = None
    status: str = "running"  # running, completed, failed
    documents_found: int = 0
    documents_downloaded: int = 0
    errors: List[dict] = field(default_factory=list)

    def mark_complete(self):
        """완료 표시"""
        self.finished_at = datetime.now()
        self.status = "completed"

    def mark_failed(self, error: Exception):
        """실패 표시"""
        self.finished_at = datetime.now()
        self.status = "failed"
        self.errors.append({
            "timestamp": datetime.now().isoformat(),
            "error": str(error),
            "type": type(error).__name__
        })

    @property
    def duration(self) -> Optional[float]:
        """실행 시간 (초)"""
        if self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None

    @property
    def success_rate(self) -> float:
        """성공률"""
        if self.documents_found == 0:
            return 0.0
        return self.documents_downloaded / self.documents_found
```

**왜 이렇게 설계했나?**

1. **Enum 사용**:
   - 타입 안전성 (오타 방지)
   - IDE 자동완성
   - 유효성 검증 자동

2. **dataclass 사용**:
   - 보일러플레이트 감소
   - 자동 `__init__`, `__repr__`
   - Type hints 강제

3. **불변성 고려**:
   - 핵심 필드는 불변
   - 계산된 값은 property

4. **유효성 검증**:
   - `__post_init__`에서 즉시 검증
   - 잘못된 데이터 조기 발견

5. **메타데이터 추적**:
   - 디버깅 용이
   - 품질 모니터링
   - 성능 분석

---

### Component 2: Database Layer

**파일**: `scraper/core/database.py`

**무엇을 만드는가?**
- SQLite 데이터베이스 관리
- CRUD 연산
- 중복 방지

**어떻게 만드는가?**

```python
import sqlite3
from pathlib import Path
from typing import Optional, List
from contextlib import contextmanager
from datetime import date, datetime
import json

from ..models import Document, ScrapingRun, Jurisdiction, DocumentType

class Database:
    """
    SQLite 데이터베이스 관리

    설계 원칙:
    1. Single Responsibility: DB 접근만 담당
    2. Context Manager: 자동 커밋/롤백
    3. Parameterized Queries: SQL Injection 방지
    """

    def __init__(self, db_path: str = "data/metadata.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def get_conn(self):
        """
        컨텍스트 매니저로 안전한 DB 연결

        예:
            with db.get_conn() as conn:
                conn.execute("...")
                # 자동 commit
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # dict-like 결과
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_schema(self):
        """스키마 초기화"""
        with self.get_conn() as conn:
            # documents 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    -- 식별 정보
                    jurisdiction TEXT NOT NULL,
                    doc_type TEXT NOT NULL,
                    meeting_date DATE NOT NULL,

                    -- 문서 정보
                    title TEXT NOT NULL,
                    source_url TEXT NOT NULL,

                    -- 파일 정보
                    file_path TEXT,
                    file_size INTEGER,
                    checksum TEXT,

                    -- 메타데이터
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata JSON,

                    -- 제약 조건
                    UNIQUE(jurisdiction, source_url)
                )
            """)

            # 인덱스 생성 (성능)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_jurisdiction
                ON documents(jurisdiction)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_meeting_date
                ON documents(meeting_date)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_checksum
                ON documents(checksum)
            """)

            # scraping_runs 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scraping_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jurisdiction TEXT NOT NULL,
                    run_type TEXT NOT NULL,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    finished_at TIMESTAMP,
                    status TEXT,
                    documents_found INTEGER DEFAULT 0,
                    documents_downloaded INTEGER DEFAULT 0,
                    errors JSON
                )
            """)

            # rules 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jurisdiction TEXT NOT NULL UNIQUE,
                    selectors JSON NOT NULL,
                    patterns JSON,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    validated BOOLEAN DEFAULT 0,
                    validation_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0
                )
            """)

    # ===== Documents CRUD =====

    def insert_document(self, doc: Document) -> Optional[int]:
        """
        문서 삽입 (중복 시 무시)

        Returns:
            int: 삽입된 row ID (중복이면 None)
        """
        with self.get_conn() as conn:
            try:
                cursor = conn.execute("""
                    INSERT INTO documents
                    (jurisdiction, doc_type, meeting_date, title, source_url,
                     file_path, file_size, checksum, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    doc.jurisdiction.value,
                    doc.doc_type.value,
                    doc.meeting_date.isoformat(),
                    doc.title,
                    doc.url,
                    doc.file_path,
                    doc.file_size,
                    doc.checksum,
                    json.dumps(doc.metadata) if doc.metadata else None
                ))
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # 중복 (UNIQUE 제약 위반)
                return None

    def get_document_by_url(self, url: str) -> Optional[Document]:
        """URL로 문서 조회"""
        with self.get_conn() as conn:
            row = conn.execute("""
                SELECT * FROM documents WHERE source_url = ?
            """, (url,)).fetchone()

            if row:
                return self._row_to_document(row)
            return None

    def get_documents(
        self,
        jurisdiction: Optional[Jurisdiction] = None,
        since: Optional[date] = None,
        doc_type: Optional[DocumentType] = None,
        limit: Optional[int] = None
    ) -> List[Document]:
        """
        문서 목록 조회 (필터링)

        Args:
            jurisdiction: 지자체 필터
            since: 날짜 이후
            doc_type: 문서 타입 필터
            limit: 최대 개수
        """
        query = "SELECT * FROM documents WHERE 1=1"
        params = []

        if jurisdiction:
            query += " AND jurisdiction = ?"
            params.append(jurisdiction.value)

        if since:
            query += " AND meeting_date >= ?"
            params.append(since.isoformat())

        if doc_type:
            query += " AND doc_type = ?"
            params.append(doc_type.value)

        query += " ORDER BY meeting_date DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        with self.get_conn() as conn:
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_document(row) for row in rows]

    def get_last_scrape_date(self, jurisdiction: Jurisdiction) -> Optional[date]:
        """마지막 스크래핑 날짜 조회"""
        with self.get_conn() as conn:
            row = conn.execute("""
                SELECT MAX(meeting_date) as last_date
                FROM documents
                WHERE jurisdiction = ?
            """, (jurisdiction.value,)).fetchone()

            if row and row['last_date']:
                return date.fromisoformat(row['last_date'])
            return None

    def count_documents(
        self,
        jurisdiction: Optional[Jurisdiction] = None,
        doc_type: Optional[DocumentType] = None
    ) -> int:
        """문서 개수 카운트"""
        query = "SELECT COUNT(*) as count FROM documents WHERE 1=1"
        params = []

        if jurisdiction:
            query += " AND jurisdiction = ?"
            params.append(jurisdiction.value)

        if doc_type:
            query += " AND doc_type = ?"
            params.append(doc_type.value)

        with self.get_conn() as conn:
            row = conn.execute(query, params).fetchone()
            return row['count']

    def _row_to_document(self, row: sqlite3.Row) -> Document:
        """DB Row → Document 객체 변환"""
        return Document(
            url=row['source_url'],
            title=row['title'],
            doc_type=DocumentType(row['doc_type']),
            meeting_date=date.fromisoformat(row['meeting_date']),
            jurisdiction=Jurisdiction(row['jurisdiction']),
            file_path=row['file_path'],
            file_size=row['file_size'],
            checksum=row['checksum'],
            scraped_at=datetime.fromisoformat(row['scraped_at']) if row['scraped_at'] else None,
            metadata=json.loads(row['metadata']) if row['metadata'] else {}
        )

    # ===== Statistics =====

    def get_statistics(self) -> dict:
        """전체 통계"""
        with self.get_conn() as conn:
            # 지자체별 문서 수
            by_jurisdiction = conn.execute("""
                SELECT jurisdiction, COUNT(*) as count
                FROM documents
                GROUP BY jurisdiction
            """).fetchall()

            # 문서 타입별 수
            by_type = conn.execute("""
                SELECT doc_type, COUNT(*) as count
                FROM documents
                GROUP BY doc_type
            """).fetchall()

            # 전체 통계
            total = conn.execute("""
                SELECT
                    COUNT(*) as total_documents,
                    SUM(file_size) as total_size
                FROM documents
            """).fetchone()

            return {
                "total_documents": total['total_documents'],
                "total_size_bytes": total['total_size'] or 0,
                "by_jurisdiction": {row['jurisdiction']: row['count'] for row in by_jurisdiction},
                "by_type": {row['doc_type']: row['count'] for row in by_type}
            }
```

**왜 이렇게 설계했나?**

1. **Context Manager**:
   - 자동 커밋/롤백
   - 연결 누수 방지

2. **Parameterized Queries**:
   - SQL Injection 방지
   - 타입 안전성

3. **UNIQUE 제약조건**:
   - 중복 방지 (jurisdiction + source_url)
   - DB 레벨 보장

4. **인덱스**:
   - 빠른 조회 (jurisdiction, meeting_date)
   - 대용량 데이터 대비

5. **통계 메서드**:
   - 모니터링 용이
   - 진행 상황 추적

---

### Component 3: LLM Agent

**파일**: `scraper/core/llm_agent.py`

**무엇을 만드는가?**
- Claude API 통합
- HTML 구조 분석
- CSS Selector 생성

**어떻게 만드는가?**

```python
import os
import json
from typing import Dict, Optional
from anthropic import Anthropic
import logging

logger = logging.getLogger(__name__)

class LLMAgent:
    """
    LLM을 사용한 페이지 분석 에이전트

    설계 원칙:
    1. Single Purpose: HTML 분석만
    2. Cost Awareness: 토큰 사용량 추적
    3. Error Handling: 명확한 에러 메시지
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = model
        self.total_cost = 0.0  # 누적 비용 추적

    def analyze_page_structure(
        self,
        html: str,
        goal: str,
        max_html_length: int = 10000
    ) -> Dict:
        """
        HTML 페이지 구조 분석하여 CSS selectors 생성

        Args:
            html: 분석할 HTML
            goal: 목표 (예: "Find all meeting minutes links")
            max_html_length: HTML 최대 길이 (비용 절감)

        Returns:
            {
                "selectors": {
                    "meeting_rows": "...",
                    "date": "...",
                    "title": "...",
                    "document_links": "..."
                },
                "date_format": "MM/DD/YYYY",
                "confidence": 0.95,
                "notes": "..."
            }
        """
        # HTML 크기 제한 (비용 절감)
        if len(html) > max_html_length:
            logger.warning(f"HTML truncated from {len(html)} to {max_html_length} chars")
            html = html[:max_html_length]

        # 프롬프트 구성
        prompt = self._build_prompt(html, goal)

        try:
            # API 호출
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0,  # Deterministic
                messages=[{"role": "user", "content": prompt}]
            )

            # 응답 파싱
            result = self._parse_response(response)

            # 비용 계산
            cost = self._calculate_cost(response.usage)
            self.total_cost += cost

            logger.info(f"LLM Analysis - Cost: ${cost:.4f}, Confidence: {result.get('confidence', 0)}")

            return result

        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            raise

    def _build_prompt(self, html: str, goal: str) -> str:
        """
        프롬프트 생성

        설계 결정:
        - Few-shot 예시 포함
        - JSON 형식 강제
        - 명확한 지시사항
        """
        return f"""You are a web scraping expert. Analyze this HTML page and extract CSS selectors.

GOAL: {goal}

REQUIREMENTS:
1. Return ONLY valid JSON (no markdown, no explanation)
2. Provide specific CSS selectors for each element
3. Include confidence score (0.0-1.0)
4. Add brief notes about the page structure

HTML:
```html
{html}
```

OUTPUT FORMAT (JSON only):
{{
  "selectors": {{
    "meeting_rows": "CSS selector for each meeting row (e.g., 'table.calendar tbody tr')",
    "date": "CSS selector for date within a row (e.g., 'td.date' or 'td:first-child')",
    "title": "CSS selector for meeting title",
    "document_links": "CSS selector for document links (e.g., 'a[href$=\\".pdf\\"]')"
  }},
  "date_format": "Detected date format (e.g., 'MM/DD/YYYY', 'YYYY-MM-DD')",
  "confidence": 0.95,
  "notes": "Brief explanation of page structure and any caveats"
}}

EXAMPLES:
{{
  "selectors": {{
    "meeting_rows": "table.meetings tbody tr",
    "date": "td:first-child",
    "title": "td:nth-child(2)",
    "document_links": "a.pdf-link"
  }},
  "date_format": "MM/DD/YYYY",
  "confidence": 0.92,
  "notes": "Standard table layout with dates in first column"
}}

NOW ANALYZE THE HTML ABOVE:"""

    def _parse_response(self, response) -> Dict:
        """
        LLM 응답 파싱

        처리:
        1. 마크다운 코드 블록 제거
        2. JSON 파싱
        3. 유효성 검증
        """
        result_text = response.content[0].text

        # 마크다운 코드 블록 제거
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]

        # JSON 파싱
        try:
            result = json.loads(result_text.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Response: {result_text}")
            raise ValueError(f"Invalid JSON from LLM: {e}")

        # 유효성 검증
        self._validate_result(result)

        return result

    def _validate_result(self, result: Dict):
        """결과 유효성 검증"""
        required_keys = ['selectors', 'confidence']
        for key in required_keys:
            if key not in result:
                raise ValueError(f"Missing required key: {key}")

        required_selectors = ['meeting_rows', 'date']
        for key in required_selectors:
            if key not in result['selectors']:
                raise ValueError(f"Missing required selector: {key}")

        if not 0.0 <= result['confidence'] <= 1.0:
            raise ValueError(f"Invalid confidence: {result['confidence']}")

    def _calculate_cost(self, usage) -> float:
        """
        비용 계산 (Claude 3.5 Sonnet 기준)

        가격:
        - Input: $3.00 / 1M tokens
        - Output: $15.00 / 1M tokens
        """
        input_cost = usage.input_tokens * 0.003 / 1000
        output_cost = usage.output_tokens * 0.015 / 1000
        return input_cost + output_cost

    def get_total_cost(self) -> float:
        """누적 비용 조회"""
        return self.total_cost
```

**왜 이렇게 설계했나?**

1. **비용 추적**:
   - 토큰 사용량 로깅
   - 누적 비용 계산
   - 예산 관리 가능

2. **HTML 크기 제한**:
   - 10,000자로 제한
   - 비용 절감
   - 응답 속도 향상

3. **Temperature = 0**:
   - Deterministic 응답
   - 재현 가능
   - 테스트 용이

4. **Few-shot 프롬프트**:
   - 정확도 향상
   - 일관된 출력 형식

5. **유효성 검증**:
   - 잘못된 응답 조기 발견
   - 명확한 에러 메시지

---

이제 나머지 컴포넌트들을 계속 작성하겠습니다. 다음에는:
- Component 4: Rule Cache
- Component 5: Storage Manager
- Component 6: Base Scraper
- Component 7: Concrete Scrapers (Cherokee, etc.)

계속 진행할까요?
