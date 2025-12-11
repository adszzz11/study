# Phase 2: 확장 개발

> 나머지 3개 지자체와 3개 문서 타입 추가, Continuous Update 구현

## 🎯 Phase 목표

**주요 목표:**
1. ✅ 나머지 3개 지자체 스크래퍼 추가
2. ✅ 모든 문서 타입 (Agendas, Packets, Videos) 지원
3. ✅ Continuous Update 모드 구현
4. ✅ 통합 테스트 및 품질 검증
5. ✅ 에러 핸들링 강화

**예상 기간**: 3-4일 (24-32시간)

**성공 기준:**
- 4개 지자체 모두 동작
- 3가지 이상 문서 타입 수집
- Continuous Update 모드 동작
- 전체 시스템 안정성 검증
- LLM 비용 $40 이하 (총)

---

## 📋 Step-by-Step 실행 계획

### Step 1: 2번째 지자체 추가 (Alpharetta) (4-5시간)

**이유**: Phase 0 조사에서 Cherokee와 유사한 구조로 판단됨

#### 1.1 Alpharetta Scraper 구현

**파일**: `scraper/jurisdictions/alpharetta.py`

```python
from typing import List, Optional
from datetime import date

from ..core.base_scraper import BaseScraper
from ..models import Meeting, Document, Jurisdiction
# Cherokee와 유사한 로직 재사용

class AlpharettaScraper(BaseScraper):
    """City of Alpharetta 스크래퍼"""

    def __init__(self):
        super().__init__(Jurisdiction.ALPHARETTA)
        # Cherokee와 동일한 컴포넌트 재사용
        self.llm = LLMAgent()
        self.rule_cache = RuleCache()

    def get_meeting_list_url(self) -> str:
        return "http://..."  # Phase 0에서 조사한 URL

    # 나머지 메서드는 Cherokee 패턴 참고하여 구현
```

**체크리스트:**
- [ ] `jurisdictions/alpharetta.py` 생성
- [ ] 기본 메서드 구현
- [ ] 테스트 (dry-run)
- [ ] 10개 이상 문서 다운로드 확인

---

### Step 2: 3번째 지자체 추가 (Holly Springs) (5-6시간)

**도전**: 동적 렌더링 (React/Vue)

#### 2.1 Playwright 통합

**수정**: `scraper/core/base_scraper.py`

```python
from playwright.sync_api import sync_playwright

def fetch_html_dynamic(self, url: str) -> str:
    """Playwright를 사용한 동적 페이지 렌더링"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")

        # 특정 요소 대기 (필요 시)
        # page.wait_for_selector("table.meetings")

        html = page.content()
        browser.close()
        return html
```

#### 2.2 Holly Springs Scraper

**파일**: `scraper/jurisdictions/holly_springs.py`

```python
class HollySpringScraper(BaseScraper):
    """City of Holly Springs 스크래퍼 (동적 사이트)"""

    def fetch_html(self, url: str) -> str:
        """Playwright 사용"""
        return self.fetch_html_dynamic(url)

    # 나머지는 유사
```

**체크리스트:**
- [ ] Playwright 통합
- [ ] `jurisdictions/holly_springs.py` 생성
- [ ] 동적 렌더링 테스트
- [ ] 문서 다운로드 확인

---

### Step 3: 4번째 지자체 추가 (Marietta) (6-8시간)

**도전**: 가장 복잡한 구조

**전략**:
1. Phase 0 분석 재검토
2. 필요 시 LLM에게 더 복잡한 분석 요청
3. Custom 로직 구현

**체크리스트:**
- [ ] Phase 0 분석 재검토
- [ ] `jurisdictions/marietta.py` 생성
- [ ] 특수 케이스 처리
- [ ] 테스트 및 검증

---

### Step 4: 추가 문서 타입 지원 (3-4시간)

#### 4.1 Agenda 수집

**수정**: `scraper/jurisdictions/cherokee.py` (및 다른 스크래퍼)

```python
def parse_documents(self, meeting: Meeting) -> List[Document]:
    """Minutes와 Agenda 모두 수집"""
    # 기존 로직에 Agenda 분류 추가

    for link in links:
        text = link.text.lower()

        if 'minute' in text:
            doc_type = DocumentType.MINUTES
        elif 'agenda' in text:
            if 'packet' in text:
                doc_type = DocumentType.PACKET
            else:
                doc_type = DocumentType.AGENDA
        # ...
```

**체크리스트:**
- [ ] Agenda 분류 로직 추가
- [ ] 4개 지자체 모두 업데이트
- [ ] Agenda 다운로드 테스트

---

#### 4.2 Packet 수집

**도전**: 대용량 PDF

**수정**: `scraper/core/storage.py`

```python
def download_document(self, doc: Document, timeout: float = 120.0) -> bool:
    """대용량 PDF를 위해 timeout 증가"""
    # Packet은 timeout을 더 길게
    if doc.doc_type == DocumentType.PACKET:
        timeout = 180.0  # 3분

    # 스트리밍 다운로드 (메모리 절약)
    with httpx.stream('GET', doc.url, timeout=timeout) as response:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
```

**체크리스트:**
- [ ] Packet 분류 로직
- [ ] 스트리밍 다운로드 구현
- [ ] 대용량 파일 테스트

---

#### 4.3 Video 링크 수집

**전략**: PDF 다운로드 대신 링크만 저장

**수정**: `scraper/core/storage.py`

```python
def save_video_link(self, doc: Document) -> bool:
    """비디오 링크를 JSON 파일로 저장"""
    file_path = self.get_file_path(doc).with_suffix('.json')

    data = {
        "url": doc.url,
        "title": doc.title,
        "platform": self.detect_platform(doc.url),  # Granicus, YouTube, Vimeo
        "meeting_date": doc.meeting_date.isoformat()
    }

    file_path.write_text(json.dumps(data, indent=2))
    doc.file_path = str(file_path)
    return True

def detect_platform(self, url: str) -> str:
    """비디오 플랫폼 감지"""
    if 'granicus' in url.lower():
        return 'Granicus'
    elif 'youtube' in url.lower() or 'youtu.be' in url.lower():
        return 'YouTube'
    elif 'vimeo' in url.lower():
        return 'Vimeo'
    else:
        return 'Unknown'
```

**체크리스트:**
- [ ] Video 링크 분류
- [ ] save_video_link 메서드
- [ ] 플랫폼 감지 로직
- [ ] JSON 저장 테스트

---

### Step 5: Continuous Update 모드 구현 (4-5시간)

#### 5.1 마지막 실행 날짜 추적

**수정**: `scraper/core/database.py`

```python
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
```

---

#### 5.2 증분 스크래핑

**수정**: `main.py`

```python
def continuous_mode(jurisdiction: str):
    """Continuous update 모드"""
    logger.info(f"=== Continuous update mode for {jurisdiction} ===")

    scraper = get_scraper(jurisdiction)
    db = Database()
    storage = Storage()

    # 마지막 스크래핑 날짜 조회
    last_date = db.get_last_scrape_date(scraper.jurisdiction)

    if last_date:
        since_date = last_date
        logger.info(f"Last scrape: {last_date}, checking for new documents")
    else:
        since_date = date.today() - timedelta(days=30)
        logger.info(f"First run, backfilling from {since_date}")

    # 스크래핑
    documents = scraper.scrape(since=since_date)

    if not documents:
        logger.info("No new documents found")
        return

    logger.info(f"Found {len(documents)} new documents")

    # 다운로드
    for doc in documents:
        if storage.download_document(doc):
            db.insert_document(doc)
```

**체크리스트:**
- [ ] get_last_scrape_date 구현
- [ ] continuous_mode 함수
- [ ] CLI에 --continuous 플래그 추가
- [ ] 테스트 (중복 방지 확인)

---

#### 5.3 스케줄링 (간단 버전)

**파일**: `scheduler.py`

```python
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

from main import continuous_mode

logger = logging.getLogger(__name__)

def scheduled_scrape():
    """모든 지자체를 순차적으로 스크래핑"""
    jurisdictions = ['cherokee', 'holly_springs', 'alpharetta', 'marietta']

    for jur in jurisdictions:
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Scheduled scrape: {jur}")
            logger.info(f"{'='*60}\n")
            continuous_mode(jur)
        except Exception as e:
            logger.error(f"Error scraping {jur}: {e}", exc_info=True)

def main():
    scheduler = BlockingScheduler()

    # 매일 새벽 2시에 실행
    scheduler.add_job(scheduled_scrape, 'cron', hour=2)

    logger.info("Scheduler started. Will run daily at 2 AM")
    logger.info("Press Ctrl+C to exit")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")

if __name__ == "__main__":
    main()
```

**체크리스트:**
- [ ] `scheduler.py` 생성
- [ ] APScheduler 설정
- [ ] 테스트 (수동 실행)
- [ ] cron 설정 문서화

---

### Step 6: 통합 테스트 및 품질 검증 (3-4시간)

#### 6.1 전체 시스템 테스트

**테스트 스크립트**: `tests/test_integration.py`

```python
import pytest
from datetime import date, timedelta

def test_all_jurisdictions():
    """모든 지자체 테스트"""
    jurisdictions = ['cherokee', 'holly_springs', 'alpharetta', 'marietta']

    for jur in jurisdictions:
        scraper = get_scraper(jur)
        documents = scraper.scrape(since=date.today() - timedelta(days=30))

        assert len(documents) > 0, f"No documents found for {jur}"
        print(f"✅ {jur}: {len(documents)} documents")

def test_all_document_types():
    """모든 문서 타입 테스트"""
    # Cherokee에서 모든 타입 수집
    scraper = CherokeeScraper()
    documents = scraper.scrape(since=date.today() - timedelta(days=180))

    types = {doc.doc_type for doc in documents}

    assert DocumentType.MINUTES in types
    assert DocumentType.AGENDA in types
    # Packet과 Video는 선택적

def test_continuous_update():
    """Continuous update 테스트"""
    # 첫 실행
    continuous_mode('cherokee')

    # 재실행 (중복 방지 확인)
    continuous_mode('cherokee')

    # DB 확인: 중복 없어야 함
```

**체크리스트:**
- [ ] 모든 지자체 테스트
- [ ] 모든 문서 타입 테스트
- [ ] Continuous update 테스트
- [ ] 중복 방지 확인

---

#### 6.2 에러 핸들링 강화

**수정**: 모든 스크래퍼

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class BaseScraper(ABC):

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def fetch_html(self, url: str) -> str:
        """재시도 로직 포함"""
        try:
            response = httpx.get(url, timeout=30.0)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            raise
```

**체크리스트:**
- [ ] tenacity로 재시도 로직 추가
- [ ] 네트워크 에러 처리
- [ ] LLM 에러 처리
- [ ] 파싱 에러 처리

---

### Step 7: 성능 최적화 (2-3시간)

#### 7.1 병렬 다운로드

**파일**: `scraper/core/parallel_downloader.py`

```python
import asyncio
import httpx

async def download_documents_parallel(documents: List[Document], max_concurrent: int = 5):
    """병렬 다운로드"""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def download_one(doc: Document):
        async with semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(doc.url, timeout=60.0)
                # 저장 로직
                ...

    tasks = [download_one(doc) for doc in documents]
    await asyncio.gather(*tasks)
```

**체크리스트:**
- [ ] 비동기 다운로드 구현
- [ ] 동시 연결 수 제한
- [ ] 성능 측정 (before/after)

---

#### 7.2 LLM 비용 최적화

**전략**:
- 규칙 캐싱 적극 활용
- HTML 크기 최소화 (필요한 부분만)
- 신뢰도 낮은 규칙만 재분석

**체크리스트:**
- [ ] 규칙 검증 로직 추가
- [ ] HTML 전처리 (불필요한 부분 제거)
- [ ] 비용 모니터링 추가

---

## 📊 Phase 2 완료 체크리스트

### 지자체 확장
- [ ] Alpharetta 스크래퍼 완성
- [ ] Holly Springs 스크래퍼 완성 (동적)
- [ ] Marietta 스크래퍼 완성
- [ ] 4개 모두 테스트 성공

### 문서 타입
- [ ] Minutes (Phase 1에서 완료)
- [ ] Agendas 수집 성공
- [ ] Packets 수집 성공
- [ ] Video 링크 저장 성공

### Continuous Update
- [ ] 마지막 실행 날짜 추적
- [ ] 증분 스크래핑 동작
- [ ] 중복 방지 확인
- [ ] 스케줄러 구현

### 품질
- [ ] 통합 테스트 통과
- [ ] 에러 핸들링 강화
- [ ] 성능 최적화
- [ ] LLM 비용 $40 이하

---

## 🎯 성공 기준

### 최소 성공
- ✅ 3개 이상 지자체 동작
- ✅ 2개 이상 문서 타입
- ✅ Continuous update 기본 동작
- ✅ 총 100개 이상 문서 수집

### 이상적 성공
- ✅ 4개 모두 안정적 동작
- ✅ 4가지 문서 타입 모두 지원
- ✅ Continuous update + 스케줄러
- ✅ 300개 이상 문서 수집
- ✅ 비용 효율적 (LLM $30 이하)

---

## ⚠️ 주의사항

### 지자체 추가 시
- **점진적 추가**: 한 번에 하나씩
- **패턴 재사용**: Cherokee 패턴 최대한 활용
- **테스트 우선**: 각 지자체 추가 후 즉시 테스트

### 성능 최적화
- **조기 최적화 금지**: 동작 확인 후 최적화
- **측정 필수**: 최적화 전후 비교
- **Rate limiting 주의**: 사이트 부하 고려

---

## 📝 산출물 (Deliverables)

1. **확장된 코드**
   - 4개 지자체 스크래퍼
   - 4개 문서 타입 지원
   - Continuous update

2. **데이터**
   - 4개 지자체 문서 (100-400개)
   - 완전한 메타데이터 DB
   - LLM 규칙 (4개)

3. **문서**
   - 업데이트된 README
   - 테스트 리포트
   - 비용 리포트

---

**다음 단계**: [Phase 3: 완성 및 제출](./phase-3-completion.md)

**작성일**: 2025-12-11
**예상 완료**: Phase 2 시작 후 3-4일
