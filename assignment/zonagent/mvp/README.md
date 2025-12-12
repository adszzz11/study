# ZonAgent - Georgia Municipal Meeting Document Scraper

> Phase 1-2: Cherokee County + City of Marietta

## 프로젝트 개요

Georgia 지자체의 Planning & Zoning 회의 문서를 자동으로 수집하는 Agentic Document Scraper.

### 지원 지자체

- ✅ Cherokee County (Granicus 플랫폼)
- ✅ City of Marietta (CivicEngage 플랫폼)
- ⏳ City of Alpharetta (Phase 3)
- ⏳ City of Holly Springs (Phase 3)

### 목표

- ✅ 2개 지자체 완전 동작
- ✅ 3가지 문서 타입 (Agenda, Minutes, Packets)
- ✅ Backfill 모드 (과거 데이터 수집)
- ✅ SQLite 데이터베이스
- ✅ 단순한 기술 스택 (httpx + BeautifulSoup)

### 기술 스택

```python
# Core
Python 3.11+
httpx          # HTTP 요청
BeautifulSoup4 # HTML 파싱
SQLite3        # 데이터베이스

# Optional (향후)
anthropic      # LLM 통합
```

## 디렉터리 구조

```
mvp/
├── src/
│   ├── models.py           # 데이터 모델 (Document, Jurisdiction 등)
│   ├── database.py         # SQLite 데이터베이스 레이어
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py         # BaseScraper 추상 클래스
│   │   └── cherokee.py     # CherokeeScraper 구현
│   ├── utils.py            # 유틸리티 함수
│   ├── config.py           # 설정 관리
│   └── main.py             # CLI 진입점
├── tests/                  # 테스트 (선택)
├── data/                   # 데이터 저장소 (생성됨)
│   ├── documents.db        # SQLite DB
│   └── downloads/          # 다운로드된 파일
├── requirements.txt        # 패키지 의존성
├── .env.example           # 환경 변수 예시
└── README.md              # 이 파일
```

## 설치 및 실행

### 1. 환경 설정

```bash
# mvp 디렉터리로 이동
cd /Users/leetangle/code/Note/assignment/zonagent/mvp

# 가상환경 생성 (권장)
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 실행

```bash
# Cherokee County 데이터 수집
python -m src.main backfill --jurisdiction cherokee

# Marietta 데이터 수집 (최근 10개)
python -m src.main backfill --jurisdiction marietta --limit 10

# 통계 확인 (모든 지자체)
python -m src.main stats

# 특정 지자체 문서 목록
python -m src.main list --jurisdiction marietta --limit 20

# 도움말
python -m src.main --help
```

## 구현 상태

### Phase 1: Cherokee County (완료) ✅

- [x] 프로젝트 구조 생성
- [x] 데이터 모델 구현
- [x] 데이터베이스 레이어
- [x] BaseScraper 추상 클래스
- [x] CherokeeScraper 구현
- [x] CLI 인터페이스
- [x] 로깅 시스템

### Phase 2: Marietta (완료) ✅

- [x] MariettaScraper 구현
- [x] CivicEngage 플랫폼 지원
- [x] 날짜 파싱 (자연어 + URL)
- [x] Packet 문서 타입 지원
- [x] 멀티 지자체 CLI 통합
- [x] 스크래퍼 팩토리 패턴

### Phase 3: Alpharetta + Holly Springs (예정) ⏳

- [ ] Playwright 통합
- [ ] CivicClerk SPA 처리
- [ ] 코드 재사용 (동일 플랫폼)

## 설계 결정

### 왜 Cherokee County인가?

1. **서버 렌더링**: Playwright 불필요 → 단순함
2. **명확한 구조**: HTML 테이블 → CSS Selector 명확
3. **빠른 개발**: 예상 4-6시간 (50% 단축)
4. **낮은 복잡도**: MVP 철학에 부합

### 기술 선택

**httpx vs requests**:
- httpx: 비동기 지원, 더 현대적
- HTTP/2 지원

**SQLite vs PostgreSQL**:
- SQLite: MVP에 충분
- 파일 기반 → 설정 간단
- Phase 2에서 PostgreSQL로 마이그레이션

**BeautifulSoup vs lxml**:
- BeautifulSoup: 더 쉬운 API
- lxml: parser로 사용

## Cherokee County 상세

### URL
https://cherokeega.granicus.com/ViewPublisher.php?view_id=1

### HTML 구조

```html
<table class="listingTable">
  <tr class="listingRow">
    <td class="listItem">Planning Commission Meeting</td>
    <td class="listItem">December 12, 2025 - 3:00 PM</td>
    <td class="listItem"><a href="AgendaViewer.php?...">Agenda</a></td>
    <td class="listItem"><a href=".../minutes.pdf">Minutes</a></td>
    <td class="listItem"><a href="...">Video</a></td>
  </tr>
</table>
```

### CSS Selectors

```python
SELECTORS = {
    "meeting_table": "table.listingTable",
    "meeting_rows": "tr.listingRow",
    "meeting_name": "td.listItem:nth-child(1)",
    "meeting_date": "td.listItem:nth-child(2)",
    "agenda_link": "td.listItem:nth-child(3) a",
    "minutes_link": "td.listItem:nth-child(4) a",
    "video_link": "td.listItem:nth-child(5) a",
}
```

### 날짜 형식

**패턴**: `"Month DD, YYYY - H:MM AM/PM"`
**정규식**: `(\w+)\s+(\d{1,2}),\s+(\d{4})\s+-\s+(\d{1,2}):(\d{2})\s+(AM|PM)`
**예시**: `"December 12, 2025 - 3:00 PM"`

## 예상 시간

| 단계 | 작업 | 시간 |
|------|------|------|
| 1.1 | 기본 구조 | 1-2시간 |
| 1.2 | Cherokee 스크래퍼 | 2-3시간 |
| 1.3 | 통합 및 테스트 | 1-2시간 |
| **총계** | | **4-7시간** |

## 다음 단계 (Phase 2)

- Marietta (CivicEngage) 추가
- Continuous 모드 구현
- LLM 통합 (선택적)
- PostgreSQL 마이그레이션

---

**생성일**: 2025-12-12
**Phase**: 1 (MVP)
**상태**: 구현 시작
