# Phase 1: MVP 개발

> 1개 지자체에서 1개 문서 타입을 수집하는 완전히 동작하는 시스템 구축

## 🎯 Phase 목표

**주요 목표:**
1. ✅ Cherokee County에서 Meeting Minutes 수집
2. ✅ Hybrid Agentic 시스템 구현 (LLM + 규칙 기반)
3. ✅ 로컬 파일 시스템에 저장 + SQLite DB
4. ✅ Backfill 모드로 최근 6개월 데이터 수집
5. ✅ 10개 이상 문서 성공적으로 다운로드

**예상 기간**: 3-5일 (24-40시간)

**성공 기준:**
- 스크래퍼 완전 동작 (end-to-end)
- 최소 10개 회의록 PDF 다운로드
- 메타데이터 DB에 정확히 저장
- 에러 없이 재실행 가능
- LLM 비용 $15 이하

---

## 📋 Step-by-Step 실행 계획

### Step 1: 기본 구조 및 모델 정의 (3-4시간)

#### 1.1 데이터 모델 정의

**파일**: `scraper/models.py`

```python
from dataclasses import dataclass
from datetime import date
from typing import Optional, List
from enum import Enum

class DocumentType(Enum):
    MINUTES = "minutes"
    AGENDA = "agenda"
    PACKET = "packet"
    VIDEO = "video"

class Jurisdiction(Enum):
    CHEROKEE_COUNTY = "cherokee_county"
    HOLLY_SPRINGS = "holly_springs"
    ALPHARETTA = "alpharetta"
    MARIETTA = "marietta"

@dataclass
class Document:
    """문서 정보"""
    url: str
    title: str
    doc_type: DocumentType
    meeting_date: date
    jurisdiction: Jurisdiction
    file_path: Optional[str] = None
    checksum: Optional[str] = None
    metadata: Optional[dict] = None

@dataclass
class Meeting:
    """회의 정보"""
    date: date
    title: str
    jurisdiction: Jurisdiction
    documents: List[Document]
    url: str
    metadata: Optional[dict] = None

@dataclass
class ScrapingRule:
    """LLM이 생성한 스크래핑 규칙"""
    jurisdiction: Jurisdiction
    selectors: dict  # CSS selectors
    patterns: dict   # 정규식 패턴
    confidence: float
    created_at: date
    validated: bool = False
```

**체크리스트:**
- [ ] `models.py` 파일 생성
- [ ] DocumentType Enum 정의
- [ ] Jurisdiction Enum 정의
- [ ] Document dataclass 정의
- [ ] Meeting dataclass 정의
- [ ] ScrapingRule dataclass 정의

---

#### 1.2 데이터베이스 스키마 및 초기화

**파일**: `scraper/core/database.py`

```python
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

class Database:
    """SQLite 데이터베이스 관리"""

    def __init__(self, db_path: str = "data/metadata.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    @contextmanager
    def get_conn(self):
        """데이터베이스 연결 컨텍스트 매니저"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self):
        """데이터베이스 초기화"""
        with self.get_conn() as conn:
            # documents 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jurisdiction TEXT NOT NULL,
                    doc_type TEXT NOT NULL,
                    meeting_date DATE NOT NULL,
                    title TEXT,
                    source_url TEXT NOT NULL,
                    file_path TEXT,
                    file_size INTEGER,
                    checksum TEXT,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata JSON,
                    UNIQUE(jurisdiction, source_url)
                )
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
                    validated BOOLEAN DEFAULT 0
                )
            """)

    def insert_document(self, doc: 'Document') -> int:
        """문서 삽입 (중복 시 무시)"""
        with self.get_conn() as conn:
            cursor = conn.execute("""
                INSERT OR IGNORE INTO documents
                (jurisdiction, doc_type, meeting_date, title, source_url, file_path, checksum, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                doc.jurisdiction.value,
                doc.doc_type.value,
                doc.meeting_date.isoformat(),
                doc.title,
                doc.url,
                doc.file_path,
                doc.checksum,
                str(doc.metadata) if doc.metadata else None
            ))
            return cursor.lastrowid
```

**체크리스트:**
- [ ] `core/database.py` 파일 생성
- [ ] Database 클래스 구현
- [ ] 테이블 스키마 정의
- [ ] insert_document 메서드 구현
- [ ] 컨텍스트 매니저 구현

---

### Step 2: BaseScraper 추상 클래스 구현 (2-3시간)

**파일**: `scraper/core/base_scraper.py`

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
import logging
from ..models import Meeting, Document, Jurisdiction

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """스크래퍼 베이스 클래스"""

    def __init__(self, jurisdiction: Jurisdiction):
        self.jurisdiction = jurisdiction
        self.logger = logging.getLogger(f"{__name__}.{jurisdiction.value}")

    @abstractmethod
    def get_meeting_list_url(self) -> str:
        """회의 목록 페이지 URL 반환"""
        pass

    @abstractmethod
    def fetch_html(self, url: str) -> str:
        """HTML 가져오기 (정적 or 동적)"""
        pass

    @abstractmethod
    def parse_meetings(self, html: str, since: Optional[date] = None) -> List[Meeting]:
        """회의 목록 파싱"""
        pass

    @abstractmethod
    def parse_documents(self, meeting: Meeting) -> List[Document]:
        """회의별 문서 링크 추출"""
        pass

    def scrape(self, since: Optional[date] = None) -> List[Document]:
        """전체 스크래핑 프로세스"""
        self.logger.info(f"Starting scrape for {self.jurisdiction.value}")

        # 1. 회의 목록 페이지 가져오기
        url = self.get_meeting_list_url()
        self.logger.info(f"Fetching meeting list from {url}")
        html = self.fetch_html(url)

        # 2. 회의 목록 파싱
        meetings = self.parse_meetings(html, since=since)
        self.logger.info(f"Found {len(meetings)} meetings")

        # 3. 각 회의별 문서 추출
        all_documents = []
        for meeting in meetings:
            try:
                documents = self.parse_documents(meeting)
                all_documents.extend(documents)
                self.logger.info(f"  {meeting.date}: {len(documents)} documents")
            except Exception as e:
                self.logger.error(f"  Error parsing {meeting.date}: {e}")

        self.logger.info(f"Total documents found: {len(all_documents)}")
        return all_documents
```

**체크리스트:**
- [ ] `core/base_scraper.py` 파일 생성
- [ ] BaseScraper 추상 클래스 정의
- [ ] abstractmethod 데코레이터 사용
- [ ] scrape() 메인 로직 구현
- [ ] 로깅 설정

---

### Step 3: LLM Agent 구현 (4-5시간)

#### 3.1 LLM Agent 코어

**파일**: `scraper/core/llm_agent.py`

```python
import os
import json
from typing import Dict, Optional
from anthropic import Anthropic
import logging

logger = logging.getLogger(__name__)

class LLMAgent:
    """LLM을 사용한 페이지 분석 에이전트"""

    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"

    def analyze_page_structure(self, html: str, goal: str) -> Dict:
        """
        HTML 페이지 구조를 분석하여 CSS selectors 생성

        Args:
            html: 분석할 HTML (5000자로 제한 권장)
            goal: 목표 (예: "Find all meeting minutes links")

        Returns:
            {
                "selectors": {...},
                "confidence": 0.0-1.0,
                "notes": "..."
            }
        """
        # HTML이 너무 크면 잘라내기
        if len(html) > 10000:
            logger.warning(f"HTML too large ({len(html)} chars), truncating to 10000")
            html = html[:10000]

        prompt = f"""
You are a web scraping expert. Analyze this HTML page and extract CSS selectors.

Goal: {goal}

HTML:
```html
{html}
```

Return ONLY valid JSON (no markdown, no explanation) with this structure:
{{
  "selectors": {{
    "meeting_rows": "CSS selector for each meeting row",
    "date": "CSS selector for date within a row",
    "title": "CSS selector for title within a row",
    "document_links": "CSS selector for document links"
  }},
  "date_format": "Detected date format (e.g., MM/DD/YYYY)",
  "confidence": 0.95,
  "notes": "Brief explanation"
}}
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text

            # JSON 추출 (마크다운 코드 블록 제거)
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]

            result = json.loads(result_text.strip())

            # 비용 로깅
            cost = (response.usage.input_tokens * 0.003 / 1000 +
                    response.usage.output_tokens * 0.015 / 1000)
            logger.info(f"LLM analysis cost: ${cost:.4f}")
            logger.info(f"Confidence: {result.get('confidence', 0)}")

            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Response was: {result_text}")
            raise
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            raise
```

**체크리스트:**
- [ ] `core/llm_agent.py` 파일 생성
- [ ] LLMAgent 클래스 구현
- [ ] analyze_page_structure 메서드
- [ ] JSON 파싱 에러 핸들링
- [ ] 비용 로깅 추가

---

#### 3.2 규칙 캐싱 시스템

**파일**: `scraper/core/rule_cache.py`

```python
import json
from pathlib import Path
from typing import Optional, Dict
from ..models import Jurisdiction
import logging

logger = logging.getLogger(__name__)

class RuleCache:
    """LLM 생성 규칙 캐싱"""

    def __init__(self, cache_dir: str = "data/rules"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_rule_path(self, jurisdiction: Jurisdiction) -> Path:
        """규칙 파일 경로"""
        return self.cache_dir / f"{jurisdiction.value}.json"

    def load_rules(self, jurisdiction: Jurisdiction) -> Optional[Dict]:
        """규칙 로드"""
        path = self.get_rule_path(jurisdiction)
        if not path.exists():
            logger.info(f"No cached rules for {jurisdiction.value}")
            return None

        with open(path, 'r') as f:
            rules = json.load(f)
            logger.info(f"Loaded cached rules for {jurisdiction.value}")
            return rules

    def save_rules(self, jurisdiction: Jurisdiction, rules: Dict):
        """규칙 저장"""
        path = self.get_rule_path(jurisdiction)
        with open(path, 'w') as f:
            json.dump(rules, f, indent=2)
        logger.info(f"Saved rules for {jurisdiction.value} to {path}")

    def clear_rules(self, jurisdiction: Jurisdiction):
        """규칙 삭제 (재학습 강제)"""
        path = self.get_rule_path(jurisdiction)
        if path.exists():
            path.unlink()
            logger.info(f"Cleared rules for {jurisdiction.value}")
```

**체크리스트:**
- [ ] `core/rule_cache.py` 파일 생성
- [ ] RuleCache 클래스 구현
- [ ] load_rules 메서드
- [ ] save_rules 메서드
- [ ] clear_rules 메서드

---

### Step 4: Cherokee County Scraper 구현 (5-6시간)

**파일**: `scraper/jurisdictions/cherokee.py`

```python
from typing import List, Optional
from datetime import date, datetime
import httpx
from bs4 import BeautifulSoup
import logging

from ..core.base_scraper import BaseScraper
from ..core.llm_agent import LLMAgent
from ..core.rule_cache import RuleCache
from ..models import Meeting, Document, DocumentType, Jurisdiction

logger = logging.getLogger(__name__)

class CherokeeScraper(BaseScraper):
    """Cherokee County 스크래퍼"""

    def __init__(self):
        super().__init__(Jurisdiction.CHEROKEE_COUNTY)
        self.llm = LLMAgent()
        self.rule_cache = RuleCache()
        self.rules = None

    def get_meeting_list_url(self) -> str:
        """회의 목록 페이지 URL"""
        # Phase 0에서 조사한 실제 URL 사용
        return "http://..."  # TODO: 실제 URL로 교체

    def fetch_html(self, url: str) -> str:
        """정적 HTML 가져오기 (Cherokee는 정적 사이트)"""
        response = httpx.get(url, timeout=30.0)
        response.raise_for_status()
        return response.text

    def ensure_rules(self, sample_html: str):
        """규칙 로드 또는 LLM으로 생성"""
        # 1. 캐시된 규칙 로드 시도
        self.rules = self.rule_cache.load_rules(self.jurisdiction)

        if self.rules and self.rules.get('confidence', 0) > 0.8:
            logger.info("Using cached rules")
            return

        # 2. 규칙이 없으면 LLM으로 분석
        logger.info("No valid cached rules, analyzing with LLM...")
        self.rules = self.llm.analyze_page_structure(
            html=sample_html[:10000],  # 처음 10000자만
            goal="Find all meeting minutes, agendas, and packets with dates"
        )

        # 3. 규칙 저장
        self.rule_cache.save_rules(self.jurisdiction, self.rules)

    def parse_meetings(self, html: str, since: Optional[date] = None) -> List[Meeting]:
        """회의 목록 파싱"""
        # 규칙 확보
        self.ensure_rules(html)

        soup = BeautifulSoup(html, 'html.parser')
        meetings = []

        # LLM이 생성한 selector 사용
        selectors = self.rules.get('selectors', {})
        rows_selector = selectors.get('meeting_rows')

        if not rows_selector:
            raise ValueError("No meeting_rows selector in rules")

        rows = soup.select(rows_selector)
        logger.info(f"Found {len(rows)} rows using selector: {rows_selector}")

        for row in rows:
            try:
                # 날짜 추출
                date_elem = row.select_one(selectors.get('date', ''))
                if not date_elem:
                    continue

                meeting_date = self.parse_date(date_elem.text.strip())
                if since and meeting_date < since:
                    continue

                # 제목 추출
                title_elem = row.select_one(selectors.get('title', ''))
                title = title_elem.text.strip() if title_elem else f"Meeting {meeting_date}"

                # 회의 객체 생성
                meeting = Meeting(
                    date=meeting_date,
                    title=title,
                    jurisdiction=self.jurisdiction,
                    documents=[],
                    url=self.get_meeting_list_url(),
                    metadata={'row_html': str(row)}
                )
                meetings.append(meeting)

            except Exception as e:
                logger.error(f"Error parsing row: {e}")
                continue

        return meetings

    def parse_date(self, date_str: str) -> date:
        """날짜 파싱 (여러 형식 지원)"""
        # LLM이 감지한 형식 사용
        date_format = self.rules.get('date_format', 'MM/DD/YYYY')

        formats = [
            '%m/%d/%Y',   # 12/11/2024
            '%m-%d-%Y',   # 12-11-2024
            '%Y-%m-%d',   # 2024-12-11
            '%B %d, %Y',  # December 11, 2024
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Could not parse date: {date_str}")

    def parse_documents(self, meeting: Meeting) -> List[Document]:
        """회의별 문서 링크 추출"""
        # meeting.metadata에 저장된 row_html 파싱
        row_html = meeting.metadata.get('row_html', '')
        soup = BeautifulSoup(row_html, 'html.parser')

        documents = []
        selectors = self.rules.get('selectors', {})
        doc_selector = selectors.get('document_links', 'a')

        links = soup.select(doc_selector)

        for link in links:
            href = link.get('href', '')
            if not href or not href.endswith('.pdf'):
                continue

            # 절대 URL 변환
            if href.startswith('/'):
                base_url = "http://..."  # TODO: 실제 도메인
                href = base_url + href
            elif not href.startswith('http'):
                continue

            # 문서 타입 분류 (간단한 키워드 기반)
            text = link.text.lower()
            if 'minute' in text:
                doc_type = DocumentType.MINUTES
            elif 'agenda' in text and 'packet' not in text:
                doc_type = DocumentType.AGENDA
            elif 'packet' in text:
                doc_type = DocumentType.PACKET
            else:
                doc_type = DocumentType.MINUTES  # 기본값

            doc = Document(
                url=href,
                title=link.text.strip(),
                doc_type=doc_type,
                meeting_date=meeting.date,
                jurisdiction=self.jurisdiction
            )
            documents.append(doc)

        return documents
```

**체크리스트:**
- [ ] `jurisdictions/cherokee.py` 파일 생성
- [ ] CherokeeScraper 클래스 구현
- [ ] get_meeting_list_url 메서드
- [ ] fetch_html 메서드
- [ ] ensure_rules 메서드 (LLM 통합)
- [ ] parse_meetings 메서드
- [ ] parse_date 메서드
- [ ] parse_documents 메서드

---

### Step 5: 문서 다운로드 및 저장 (3-4시간)

**파일**: `scraper/core/storage.py`

```python
import hashlib
from pathlib import Path
from typing import Optional
import httpx
import logging

from ..models import Document

logger = logging.getLogger(__name__)

class Storage:
    """문서 다운로드 및 저장"""

    def __init__(self, base_dir: str = "data/documents"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_file_path(self, doc: Document) -> Path:
        """문서 저장 경로 생성"""
        # 계층적 구조: jurisdiction/year/month/
        year = doc.meeting_date.year
        month = f"{doc.meeting_date.month:02d}"

        dir_path = self.base_dir / doc.jurisdiction.value / str(year) / month
        dir_path.mkdir(parents=True, exist_ok=True)

        # 파일명: YYYY-MM-DD_doctype.pdf
        filename = f"{doc.meeting_date.isoformat()}_{doc.doc_type.value}.pdf"

        # 중복 시 번호 추가
        file_path = dir_path / filename
        counter = 1
        while file_path.exists():
            filename = f"{doc.meeting_date.isoformat()}_{doc.doc_type.value}_{counter}.pdf"
            file_path = dir_path / filename
            counter += 1

        return file_path

    def download_document(self, doc: Document, timeout: float = 60.0) -> bool:
        """
        문서 다운로드

        Returns:
            bool: 성공 여부
        """
        try:
            logger.info(f"Downloading: {doc.title} from {doc.url}")

            # HTTP 요청
            response = httpx.get(doc.url, timeout=timeout, follow_redirects=True)
            response.raise_for_status()

            # Content-Type 확인
            content_type = response.headers.get('content-type', '')
            if 'pdf' not in content_type.lower():
                logger.warning(f"Not a PDF: {content_type}")
                # 그래도 저장 시도

            # 파일 저장
            file_path = self.get_file_path(doc)
            file_path.write_bytes(response.content)

            # 메타데이터 업데이트
            doc.file_path = str(file_path)
            doc.checksum = self.calculate_checksum(response.content)

            logger.info(f"  ✅ Saved to {file_path} ({len(response.content)} bytes)")
            return True

        except httpx.HTTPError as e:
            logger.error(f"  ❌ HTTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"  ❌ Error: {e}")
            return False

    def calculate_checksum(self, content: bytes) -> str:
        """SHA256 체크섬 계산 (중복 방지용)"""
        return hashlib.sha256(content).hexdigest()

    def is_duplicate(self, doc: Document) -> bool:
        """중복 문서인지 확인 (checksum 기반)"""
        # TODO: DB에서 checksum 조회
        return False
```

**체크리스트:**
- [ ] `core/storage.py` 파일 생성
- [ ] Storage 클래스 구현
- [ ] get_file_path 메서드 (계층적 구조)
- [ ] download_document 메서드
- [ ] calculate_checksum 메서드
- [ ] 에러 핸들링

---

### Step 6: 메인 실행 로직 및 CLI (2-3시간)

**파일**: `main.py`

```python
#!/usr/bin/env python3
import argparse
import logging
from datetime import date, timedelta
from pathlib import Path

from scraper.jurisdictions.cherokee import CherokeeScraper
from scraper.core.database import Database
from scraper.core.storage import Storage
from scraper.models import Jurisdiction

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Zonagent Document Scraper')
    parser.add_argument('--jurisdiction', default='cherokee',
                        choices=['cherokee', 'holly_springs', 'alpharetta', 'marietta'],
                        help='Jurisdiction to scrape')
    parser.add_argument('--since', type=str,
                        help='Scrape documents since this date (YYYY-MM-DD)')
    parser.add_argument('--months', type=int, default=6,
                        help='Number of months to backfill (default: 6)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Find documents but do not download')

    args = parser.parse_args()

    # 날짜 계산
    if args.since:
        since_date = date.fromisoformat(args.since)
    else:
        since_date = date.today() - timedelta(days=30 * args.months)

    logger.info(f"=== Starting scrape for {args.jurisdiction} ===")
    logger.info(f"Since: {since_date}")

    # 스크래퍼 선택
    if args.jurisdiction == 'cherokee':
        scraper = CherokeeScraper()
    else:
        raise NotImplementedError(f"Scraper for {args.jurisdiction} not yet implemented")

    # 데이터베이스 및 스토리지
    db = Database()
    storage = Storage()

    try:
        # 1. 문서 발견
        logger.info("\n--- Phase 1: Finding documents ---")
        documents = scraper.scrape(since=since_date)
        logger.info(f"Found {len(documents)} documents")

        if not documents:
            logger.warning("No documents found!")
            return

        # 2. 문서 다운로드
        if args.dry_run:
            logger.info("\n--- Dry run mode: skipping download ---")
            for doc in documents:
                logger.info(f"  Would download: {doc.title} ({doc.url})")
            return

        logger.info("\n--- Phase 2: Downloading documents ---")
        success_count = 0
        fail_count = 0

        for i, doc in enumerate(documents, 1):
            logger.info(f"\n[{i}/{len(documents)}] {doc.title}")

            # 다운로드
            if storage.download_document(doc):
                # DB에 저장
                db.insert_document(doc)
                success_count += 1
            else:
                fail_count += 1

        # 3. 결과 요약
        logger.info("\n" + "=" * 60)
        logger.info("=== Scraping completed ===")
        logger.info(f"✅ Success: {success_count}")
        logger.info(f"❌ Failed: {fail_count}")
        logger.info(f"📊 Total: {len(documents)}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
```

**체크리스트:**
- [ ] `main.py` 파일 생성
- [ ] ArgumentParser 설정
- [ ] 로깅 설정
- [ ] 메인 로직 구현
- [ ] 에러 핸들링
- [ ] 실행 권한 부여 (`chmod +x main.py`)

---

### Step 7: 테스트 및 디버깅 (4-6시간)

#### 7.1 단위 테스트

**파일**: `tests/test_models.py`

```python
from datetime import date
from scraper.models import Document, DocumentType, Jurisdiction

def test_document_creation():
    doc = Document(
        url="http://example.com/minutes.pdf",
        title="Meeting Minutes",
        doc_type=DocumentType.MINUTES,
        meeting_date=date(2024, 12, 11),
        jurisdiction=Jurisdiction.CHEROKEE_COUNTY
    )
    assert doc.url == "http://example.com/minutes.pdf"
    assert doc.doc_type == DocumentType.MINUTES
```

**실행**:
```bash
pytest tests/ -v
```

**체크리스트:**
- [ ] 모델 테스트 작성
- [ ] 날짜 파싱 테스트
- [ ] 체크섬 테스트

---

#### 7.2 통합 테스트 (실제 사이트)

```bash
# Dry run으로 먼저 테스트
python main.py --jurisdiction cherokee --months 1 --dry-run

# 실제 다운로드 (소량)
python main.py --jurisdiction cherokee --months 1
```

**체크리스트:**
- [ ] Dry run 성공
- [ ] 1개월 데이터 다운로드 성공
- [ ] DB 저장 확인
- [ ] 파일 구조 확인

---

#### 7.3 에러 케이스 테스트

**테스트 시나리오**:
- [ ] 네트워크 에러 (잘못된 URL)
- [ ] HTML 구조 변경 (잘못된 selector)
- [ ] 중복 실행 (idempotency)
- [ ] API key 없음

---

### Step 8: 최종 점검 및 리팩토링 (2-3시간)

#### 8.1 코드 정리

**체크리스트:**
- [ ] 불필요한 주석 제거
- [ ] TODO 주석 처리
- [ ] 함수 docstring 추가
- [ ] Type hints 확인

---

#### 8.2 README 작성

**파일**: `README.md`

```markdown
# Zonagent Document Scraper - MVP

An agentic system to scrape municipal meeting documents.

## Features (MVP)

- ✅ Cherokee County support
- ✅ Meeting Minutes collection
- ✅ Hybrid Agentic approach (LLM + rule-based)
- ✅ Local storage + SQLite metadata
- ✅ Backfill mode (6 months)

## Setup

\`\`\`bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium

# 4. Set API key
echo "ANTHROPIC_API_KEY=your_key" > .env
\`\`\`

## Usage

\`\`\`bash
# Dry run (find but don't download)
python main.py --jurisdiction cherokee --months 6 --dry-run

# Actual scraping
python main.py --jurisdiction cherokee --months 6
\`\`\`

## Project Structure

\`\`\`
zonagent-scraper/
├── scraper/
│   ├── core/           # Base classes
│   ├── jurisdictions/  # Cherokee scraper
│   └── models.py
├── data/
│   ├── documents/      # Downloaded PDFs
│   ├── rules/          # LLM-generated rules
│   └── metadata.db     # SQLite database
└── main.py
\`\`\`

## Cost

- LLM analysis: ~$2-5
- Total MVP: <$10
```

**체크리스트:**
- [ ] README.md 작성
- [ ] requirements.txt 생성
- [ ] .gitignore 업데이트

---

## 📊 Phase 1 완료 체크리스트

### 코드 구현
- [ ] models.py (데이터 모델)
- [ ] core/database.py (SQLite)
- [ ] core/base_scraper.py (추상 클래스)
- [ ] core/llm_agent.py (LLM 통합)
- [ ] core/rule_cache.py (규칙 캐싱)
- [ ] core/storage.py (다운로드/저장)
- [ ] jurisdictions/cherokee.py (Cherokee 스크래퍼)
- [ ] main.py (실행 로직)

### 테스트
- [ ] 단위 테스트 작성
- [ ] Dry run 성공
- [ ] 10개 이상 문서 다운로드 성공
- [ ] 중복 실행 테스트

### 문서화
- [ ] README.md
- [ ] requirements.txt
- [ ] 코드 주석 및 docstring

### 품질
- [ ] 에러 핸들링 완비
- [ ] 로깅 완비
- [ ] LLM 비용 $15 이하

---

## 🎯 성공 기준

### 최소 성공 (제출 가능)
- ✅ Cherokee County에서 동작
- ✅ 10개 이상 Minutes PDF 다운로드
- ✅ DB에 메타데이터 저장
- ✅ 재실행 가능 (idempotent)

### 이상적 성공
- ✅ 안정적으로 동작 (에러 없음)
- ✅ LLM 규칙 생성 및 재사용
- ✅ 비용 $10 이하
- ✅ 코드 품질 우수

---

## ⚠️ 주의사항

### 개발 중
- **작은 단위로 테스트**: 한 번에 모든 기능 구현 X
- **LLM 비용 주의**: 테스트는 샘플 HTML로
- **로깅 필수**: 디버깅 위해 상세히

### 디버깅
- **HTML 저장**: 문제 발생 시 분석용
- **규칙 검증**: LLM이 생성한 selector 수동 확인
- **소량 테스트**: 처음엔 1개월 데이터만

---

## 📝 산출물 (Deliverables)

1. **동작하는 코드**
   - 완전한 MVP 스크래퍼
   - 10개 이상 문서 다운로드 성공

2. **데이터**
   - `data/documents/cherokee_county/`에 PDF 파일
   - `data/metadata.db`에 메타데이터
   - `data/rules/cherokee_county.json`에 LLM 규칙

3. **문서**
   - README.md
   - requirements.txt
   - scraper.log (실행 로그)

---

**다음 단계**: [Phase 2: 확장 개발](./phase-2-expansion.md)

**작성일**: 2025-12-11
**예상 완료**: Phase 1 시작 후 3-5일
