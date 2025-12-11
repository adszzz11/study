# 구현 로드맵 (Implementation Roadmap)

> 명세를 실제 코드로 만들어가는 구체적인 순서와 방법

## 📋 개요

이 문서는 **무엇을 어떤 순서로 만들 것인지** 구체적으로 정의합니다.
각 단계는 독립적으로 완성 가능하며, 테스트 가능합니다.

---

## 🎯 구현 전략

### Iterative Development (반복적 개발)

```
Iteration 1 (Week 1)
    ↓
  MVP (최소 기능)
    ├─ 1개 지자체
    ├─ 1개 문서 타입
    └─ 기본 동작

Iteration 2 (Week 2)
    ↓
  Extended (확장)
    ├─ 4개 지자체
    ├─ 4개 문서 타입
    └─ Continuous Update

Iteration 3 (Week 3)
    ↓
  Polished (완성)
    ├─ 문서화
    ├─ 테스트
    └─ 제출
```

### Test-Driven Development (TDD)

각 컴포넌트:
1. **테스트 작성** (먼저)
2. **구현** (테스트 통과하도록)
3. **리팩토링** (코드 개선)

---

## 📅 Iteration 1: MVP (최소 기능 제품)

**목표**: Cherokee County에서 Meeting Minutes 10개 수집

**기간**: 5-7일

### Day 1: 프로젝트 셋업 및 데이터 모델

#### Morning (4시간)
**만들 것**:
1. ✅ 프로젝트 구조 생성
2. ✅ 가상환경 및 패키지 설치
3. ✅ .env 설정

**구체적 작업**:
```bash
# 1. 프로젝트 생성
mkdir zonagent-scraper && cd zonagent-scraper

# 2. Python 환경
python -m venv venv
source venv/bin/activate

# 3. 패키지 설치
pip install anthropic playwright beautifulsoup4 httpx python-dotenv tenacity structlog pytest

# 4. Playwright 설치
playwright install chromium

# 5. 구조 생성
mkdir -p scraper/{core,jurisdictions,utils,config}
mkdir -p data/{documents,rules}
mkdir -p tests
mkdir -p docs

touch scraper/__init__.py
touch scraper/core/__init__.py
touch scraper/jurisdictions/__init__.py
```

#### Afternoon (4시간)
**만들 것**:
1. ✅ `models.py` 완성
2. ✅ 테스트 작성

**구체적 작업**:

**파일**: `scraper/models.py`
```python
# Component 1의 전체 코드 구현 (Enum, dataclass 모두)
# - DocumentType
# - Jurisdiction
# - Document
# - Meeting
# - ScrapingRule
# - ScrapingRun
```

**파일**: `tests/test_models.py`
```python
import pytest
from datetime import date
from scraper.models import (
    Document, DocumentType, Jurisdiction,
    Meeting, ScrapingRule
)

def test_document_creation():
    """기본 Document 생성 테스트"""
    doc = Document(
        url="http://example.com/minutes.pdf",
        title="Meeting Minutes",
        doc_type=DocumentType.MINUTES,
        meeting_date=date(2024, 12, 11),
        jurisdiction=Jurisdiction.CHEROKEE_COUNTY
    )
    assert doc.url == "http://example.com/minutes.pdf"
    assert doc.filename == "2024-12-11_minutes.pdf"

def test_document_type_from_text():
    """텍스트에서 문서 타입 추론"""
    assert DocumentType.from_text("Meeting Minutes") == DocumentType.MINUTES
    assert DocumentType.from_text("Agenda Packet") == DocumentType.PACKET
    assert DocumentType.from_text("Regular Agenda") == DocumentType.AGENDA

def test_meeting_add_document():
    """회의에 문서 추가"""
    meeting = Meeting(
        date=date(2024, 12, 11),
        title="Regular Meeting",
        jurisdiction=Jurisdiction.CHEROKEE_COUNTY,
        url="http://example.com"
    )

    doc = Document(
        url="http://example.com/minutes.pdf",
        title="Minutes",
        doc_type=DocumentType.MINUTES,
        meeting_date=date(2024, 12, 11),
        jurisdiction=Jurisdiction.CHEROKEE_COUNTY
    )

    meeting.add_document(doc)
    assert len(meeting.documents) == 1

def test_scraping_rule_validation():
    """규칙 유효성 검증"""
    with pytest.raises(ValueError):
        # confidence가 범위 밖
        ScrapingRule(
            jurisdiction=Jurisdiction.CHEROKEE_COUNTY,
            selectors={"meeting_rows": "tr", "date": "td"},
            confidence=1.5  # 잘못된 값
        )
```

**실행**:
```bash
pytest tests/test_models.py -v
```

**체크리스트**:
- [ ] 프로젝트 구조 생성 완료
- [ ] models.py 작성 완료
- [ ] 테스트 모두 통과

---

### Day 2: Database Layer

#### Morning (4시간)
**만들 것**:
1. ✅ `database.py` 구현
2. ✅ 스키마 초기화

**파일**: `scraper/core/database.py`
```python
# Component 2의 전체 Database 클래스 구현
# - __init__
# - _init_schema
# - insert_document
# - get_document_by_url
# - get_documents
# - get_last_scrape_date
# - get_statistics
```

#### Afternoon (4시간)
**만들 것**:
1. ✅ Database 테스트
2. ✅ 통합 테스트

**파일**: `tests/test_database.py`
```python
import pytest
from pathlib import Path
from datetime import date
from scraper.core.database import Database
from scraper.models import Document, DocumentType, Jurisdiction

@pytest.fixture
def temp_db(tmp_path):
    """임시 테스트 DB"""
    db_path = tmp_path / "test.db"
    db = Database(str(db_path))
    yield db
    # Cleanup
    if db_path.exists():
        db_path.unlink()

def test_insert_document(temp_db):
    """문서 삽입 테스트"""
    doc = Document(
        url="http://example.com/test.pdf",
        title="Test Doc",
        doc_type=DocumentType.MINUTES,
        meeting_date=date(2024, 12, 11),
        jurisdiction=Jurisdiction.CHEROKEE_COUNTY
    )

    row_id = temp_db.insert_document(doc)
    assert row_id is not None

    # 중복 삽입 시도
    row_id2 = temp_db.insert_document(doc)
    assert row_id2 is None  # 중복은 무시

def test_get_last_scrape_date(temp_db):
    """마지막 스크래핑 날짜 조회"""
    # 빈 DB
    last_date = temp_db.get_last_scrape_date(Jurisdiction.CHEROKEE_COUNTY)
    assert last_date is None

    # 문서 삽입
    doc1 = Document(
        url="http://example.com/1.pdf",
        title="Doc 1",
        doc_type=DocumentType.MINUTES,
        meeting_date=date(2024, 11, 1),
        jurisdiction=Jurisdiction.CHEROKEE_COUNTY
    )
    doc2 = Document(
        url="http://example.com/2.pdf",
        title="Doc 2",
        doc_type=DocumentType.MINUTES,
        meeting_date=date(2024, 12, 1),
        jurisdiction=Jurisdiction.CHEROKEE_COUNTY
    )

    temp_db.insert_document(doc1)
    temp_db.insert_document(doc2)

    # 최신 날짜 확인
    last_date = temp_db.get_last_scrape_date(Jurisdiction.CHEROKEE_COUNTY)
    assert last_date == date(2024, 12, 1)

def test_statistics(temp_db):
    """통계 조회 테스트"""
    # 여러 문서 삽입
    for i in range(5):
        doc = Document(
            url=f"http://example.com/{i}.pdf",
            title=f"Doc {i}",
            doc_type=DocumentType.MINUTES,
            meeting_date=date(2024, 12, i+1),
            jurisdiction=Jurisdiction.CHEROKEE_COUNTY,
            file_size=1000 * i
        )
        temp_db.insert_document(doc)

    stats = temp_db.get_statistics()
    assert stats['total_documents'] == 5
    assert stats['by_jurisdiction']['cherokee_county'] == 5
```

**실행**:
```bash
pytest tests/test_database.py -v
```

**체크리스트**:
- [ ] database.py 작성 완료
- [ ] DB 스키마 생성 확인
- [ ] 테스트 모두 통과

---

### Day 3: LLM Agent

#### Morning (4시간)
**만들 것**:
1. ✅ `llm_agent.py` 구현
2. ✅ 프롬프트 설계

**파일**: `scraper/core/llm_agent.py`
```python
# Component 3의 전체 LLMAgent 클래스 구현
# - __init__
# - analyze_page_structure
# - _build_prompt
# - _parse_response
# - _validate_result
# - _calculate_cost
```

#### Afternoon (4시간)
**만들 것**:
1. ✅ LLM Agent 테스트 (Mock)
2. ✅ 실제 HTML 샘플 테스트

**파일**: `tests/test_llm_agent.py`
```python
import pytest
from scraper.core.llm_agent import LLMAgent

@pytest.mark.skip(reason="Requires API key and costs money")
def test_analyze_real_html():
    """실제 HTML 분석 (수동 테스트용)"""
    agent = LLMAgent()

    sample_html = """
    <table class="meetings">
        <tr>
            <td class="date">12/11/2024</td>
            <td class="title">Regular Meeting</td>
            <td><a href="/minutes.pdf">Minutes</a></td>
        </tr>
    </table>
    """

    result = agent.analyze_page_structure(
        html=sample_html,
        goal="Find all meeting minutes links"
    )

    assert 'selectors' in result
    assert 'confidence' in result
    assert result['confidence'] > 0.5

def test_parse_response():
    """응답 파싱 테스트"""
    agent = LLMAgent()

    # Mock 응답
    response_text = '''```json
    {
      "selectors": {
        "meeting_rows": "table tr",
        "date": "td.date"
      },
      "confidence": 0.95
    }
    ```'''

    # 테스트용 Mock 객체
    class MockContent:
        def __init__(self, text):
            self.text = text

    class MockResponse:
        def __init__(self, text):
            self.content = [MockContent(text)]

    mock_response = MockResponse(response_text)
    result = agent._parse_response(mock_response)

    assert result['selectors']['meeting_rows'] == "table tr"
    assert result['confidence'] == 0.95
```

**체크리스트**:
- [ ] llm_agent.py 작성 완료
- [ ] 프롬프트 검증
- [ ] 파싱 로직 테스트 통과

---

### Day 4: Rule Cache & Storage

#### Morning (4시간)
**만들 것**:
1. ✅ `rule_cache.py` 구현
2. ✅ `storage.py` 구현

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
        return self.cache_dir / f"{jurisdiction.value}.json"

    def load_rules(self, jurisdiction: Jurisdiction) -> Optional[Dict]:
        path = self.get_rule_path(jurisdiction)
        if not path.exists():
            logger.info(f"No cached rules for {jurisdiction.value}")
            return None

        with open(path, 'r') as f:
            rules = json.load(f)
            logger.info(f"Loaded cached rules for {jurisdiction.value}")
            return rules

    def save_rules(self, jurisdiction: Jurisdiction, rules: Dict):
        path = self.get_rule_path(jurisdiction)
        with open(path, 'w') as f:
            json.dump(rules, f, indent=2)
        logger.info(f"Saved rules to {path}")

    def clear_rules(self, jurisdiction: Jurisdiction):
        path = self.get_rule_path(jurisdiction)
        if path.exists():
            path.unlink()
            logger.info(f"Cleared rules for {jurisdiction.value}")
```

**파일**: `scraper/core/storage.py`
```python
import hashlib
from pathlib import Path
import httpx
import logging
from ..models import Document, DocumentType

logger = logging.getLogger(__name__)

class Storage:
    """문서 다운로드 및 저장"""

    def __init__(self, base_dir: str = "data/documents"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_file_path(self, doc: Document) -> Path:
        """계층적 파일 경로 생성"""
        year = doc.meeting_date.year
        month = f"{doc.meeting_date.month:02d}"

        dir_path = self.base_dir / doc.jurisdiction.value / str(year) / month
        dir_path.mkdir(parents=True, exist_ok=True)

        filename = doc.filename
        file_path = dir_path / filename

        # 중복 파일명 처리
        counter = 1
        while file_path.exists():
            stem = file_path.stem.rsplit('_', 1)[0] if '_' in file_path.stem else file_path.stem
            file_path = dir_path / f"{stem}_{counter}{file_path.suffix}"
            counter += 1

        return file_path

    def download_document(self, doc: Document, timeout: float = 60.0) -> bool:
        try:
            logger.info(f"Downloading: {doc.title}")

            response = httpx.get(doc.url, timeout=timeout, follow_redirects=True)
            response.raise_for_status()

            file_path = self.get_file_path(doc)
            file_path.write_bytes(response.content)

            # 메타데이터 업데이트
            doc.file_path = str(file_path)
            doc.file_size = len(response.content)
            doc.checksum = self.calculate_checksum(response.content)

            logger.info(f"  ✅ Saved to {file_path} ({doc.file_size} bytes)")
            return True

        except Exception as e:
            logger.error(f"  ❌ Download failed: {e}")
            return False

    def calculate_checksum(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()
```

#### Afternoon (4시간)
**만들 것**:
1. ✅ 테스트 작성
2. ✅ 통합 테스트

**체크리스트**:
- [ ] rule_cache.py 작성 완료
- [ ] storage.py 작성 완료
- [ ] 테스트 통과

---

### Day 5-6: Base Scraper & Cherokee Scraper

#### Day 5: BaseScraper

**만들 것**:
1. ✅ `base_scraper.py` 추상 클래스
2. ✅ 공통 로직 구현

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
        """회의 목록 페이지 URL"""
        pass

    @abstractmethod
    def fetch_html(self, url: str) -> str:
        """HTML 가져오기"""
        pass

    @abstractmethod
    def parse_meetings(self, html: str, since: Optional[date] = None) -> List[Meeting]:
        """회의 목록 파싱"""
        pass

    @abstractmethod
    def parse_documents(self, meeting: Meeting) -> List[Document]:
        """회의별 문서 추출"""
        pass

    def scrape(self, since: Optional[date] = None) -> List[Document]:
        """전체 스크래핑 프로세스"""
        self.logger.info(f"Starting scrape for {self.jurisdiction.value}")

        # 1. 회의 목록 가져오기
        url = self.get_meeting_list_url()
        html = self.fetch_html(url)

        # 2. 회의 파싱
        meetings = self.parse_meetings(html, since=since)
        self.logger.info(f"Found {len(meetings)} meetings")

        # 3. 문서 추출
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

#### Day 6: Cherokee Scraper

**만들 것**:
1. ✅ `cherokee.py` 구현
2. ✅ 실제 웹사이트 테스트

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

    # Phase 0 조사에서 확인한 실제 URL
    MEETING_LIST_URL = "http://..."  # TODO: 실제 URL로 교체

    def __init__(self):
        super().__init__(Jurisdiction.CHEROKEE_COUNTY)
        self.llm = LLMAgent()
        self.rule_cache = RuleCache()
        self.rules = None

    def get_meeting_list_url(self) -> str:
        return self.MEETING_LIST_URL

    def fetch_html(self, url: str) -> str:
        """정적 HTML 가져오기"""
        response = httpx.get(url, timeout=30.0)
        response.raise_for_status()
        return response.text

    def ensure_rules(self, sample_html: str):
        """규칙 로드 또는 LLM으로 생성"""
        # 1. 캐시 시도
        self.rules = self.rule_cache.load_rules(self.jurisdiction)

        if self.rules and self.rules.get('confidence', 0) > 0.8:
            self.logger.info("Using cached rules")
            return

        # 2. LLM 분석
        self.logger.info("Analyzing page with LLM...")
        self.rules = self.llm.analyze_page_structure(
            html=sample_html[:10000],
            goal="Find all meeting minutes, agendas, and packets"
        )

        # 3. 캐시 저장
        self.rule_cache.save_rules(self.jurisdiction, self.rules)

    def parse_meetings(self, html: str, since: Optional[date] = None) -> List[Meeting]:
        """회의 목록 파싱"""
        self.ensure_rules(html)

        soup = BeautifulSoup(html, 'html.parser')
        meetings = []

        selectors = self.rules.get('selectors', {})
        rows = soup.select(selectors.get('meeting_rows', ''))

        for row in rows:
            try:
                # 날짜 추출
                date_elem = row.select_one(selectors.get('date', ''))
                if not date_elem:
                    continue

                meeting_date = self.parse_date(date_elem.text.strip())

                if since and meeting_date < since:
                    continue

                # 제목
                title_elem = row.select_one(selectors.get('title', ''))
                title = title_elem.text.strip() if title_elem else f"Meeting {meeting_date}"

                meeting = Meeting(
                    date=meeting_date,
                    title=title,
                    jurisdiction=self.jurisdiction,
                    url=self.MEETING_LIST_URL,
                    metadata={'row_html': str(row)}
                )
                meetings.append(meeting)

            except Exception as e:
                self.logger.error(f"Error parsing row: {e}")
                continue

        return meetings

    def parse_date(self, date_str: str) -> date:
        """날짜 파싱"""
        formats = [
            '%m/%d/%Y',
            '%m-%d-%Y',
            '%Y-%m-%d',
            '%B %d, %Y',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Could not parse date: {date_str}")

    def parse_documents(self, meeting: Meeting) -> List[Document]:
        """회의별 문서 링크 추출"""
        row_html = meeting.metadata.get('row_html', '')
        soup = BeautifulSoup(row_html, 'html.parser')

        documents = []
        selectors = self.rules.get('selectors', {})
        links = soup.select(selectors.get('document_links', 'a'))

        for link in links:
            href = link.get('href', '')
            if not href or not href.endswith('.pdf'):
                continue

            # 절대 URL
            if href.startswith('/'):
                href = "http://cherokee-domain.com" + href  # TODO: 실제 도메인

            # 문서 타입 분류
            doc_type = DocumentType.from_text(link.text)

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

**체크리스트**:
- [ ] base_scraper.py 완성
- [ ] cherokee.py 완성
- [ ] 실제 웹사이트에서 10개 이상 문서 발견

---

### Day 7: Main CLI & Integration

**만들 것**:
1. ✅ `main.py` CLI 구현
2. ✅ End-to-end 테스트
3. ✅ MVP 완성 검증

**파일**: `main.py`

```python
#!/usr/bin/env python3
import argparse
import logging
from datetime import date, timedelta

from scraper.jurisdictions.cherokee import CherokeeScraper
from scraper.core.database import Database
from scraper.core.storage import Storage

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
    parser = argparse.ArgumentParser(description='Zonagent Document Scraper - MVP')
    parser.add_argument('--months', type=int, default=6,
                        help='Number of months to backfill (default: 6)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Find documents but do not download')

    args = parser.parse_args()

    # 날짜 계산
    since_date = date.today() - timedelta(days=30 * args.months)

    logger.info(f"=== Zonagent Scraper MVP ===")
    logger.info(f"Jurisdiction: Cherokee County")
    logger.info(f"Since: {since_date}")

    # 초기화
    scraper = CherokeeScraper()
    db = Database()
    storage = Storage()

    try:
        # 1. 문서 발견
        logger.info("\n--- Finding documents ---")
        documents = scraper.scrape(since=since_date)
        logger.info(f"Found {len(documents)} documents")

        if not documents:
            logger.warning("No documents found!")
            return

        # 2. Dry run 확인
        if args.dry_run:
            logger.info("\n--- Dry run mode ---")
            for i, doc in enumerate(documents, 1):
                logger.info(f"{i}. {doc.title} ({doc.meeting_date})")
            return

        # 3. 다운로드
        logger.info("\n--- Downloading documents ---")
        success = 0
        failed = 0

        for i, doc in enumerate(documents, 1):
            logger.info(f"\n[{i}/{len(documents)}] {doc.title}")

            if storage.download_document(doc):
                db.insert_document(doc)
                success += 1
            else:
                failed += 1

        # 4. 결과
        logger.info("\n" + "="*60)
        logger.info("=== Scraping completed ===")
        logger.info(f"✅ Success: {success}")
        logger.info(f"❌ Failed: {failed}")
        logger.info(f"📊 Total: {len(documents)}")
        logger.info("="*60)

        # 5. 통계
        stats = db.get_statistics()
        logger.info(f"\n📈 Database Statistics:")
        logger.info(f"  Total documents: {stats['total_documents']}")
        logger.info(f"  Total size: {stats['total_size_bytes'] / 1024 / 1024:.2f} MB")

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
```

**실행**:
```bash
# Dry run
python main.py --months 6 --dry-run

# 실제 실행
python main.py --months 6
```

**체크리스트**:
- [ ] main.py 완성
- [ ] 10개 이상 PDF 다운로드 성공
- [ ] DB에 메타데이터 저장 확인
- [ ] 파일 구조 확인
- [ ] 로그 확인

---

## MVP 완료 기준

### ✅ 동작 확인
- [ ] `python main.py --dry-run` 성공
- [ ] 10개 이상 문서 발견
- [ ] 다운로드 성공 (80% 이상)
- [ ] DB에 저장 확인

### ✅ 코드 품질
- [ ] 모든 테스트 통과
- [ ] 타입 힌트 완성
- [ ] Docstring 작성

### ✅ 문서화
- [ ] README.md 기본 작성
- [ ] 실행 방법 문서화

---

**다음 단계**: Iteration 2 (나머지 지자체 추가)

**작성일**: 2025-12-11
**예상 완료**: Day 7 (1주일)
