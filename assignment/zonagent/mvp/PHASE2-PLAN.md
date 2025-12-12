# Phase 2 실행 계획

> **목표**: 2개 지자체 지원 (Cherokee + Marietta)
> **예상 기간**: 3-4시간
> **상태**: 🟡 시작

---

## 🎯 Phase 2 목표

Phase 1의 Cherokee County에 Marietta를 추가하여 2개 지자체를 지원합니다.

### 핵심 목표

1. ✅ Marietta (CivicEngage) 스크래퍼 추가
2. ✅ 멀티 지자체 지원 검증
3. ✅ CLI에서 두 지자체 선택 가능
4. ⏳ Continuous 모드 (선택)

---

## 📊 Marietta 분석 요약

### 기본 정보

- **URL**: https://www.mariettaga.gov/AgendaCenter
- **플랫폼**: CivicEngage (Agenda Center)
- **렌더링**: 🟡 하이브리드 (서버 + jQuery)
- **난이도**: 🟢 쉬움
- **평가**: ⭐⭐⭐⭐

### 기술적 특징

**장점**:
- ✅ 서버에서 완전한 HTML 생성 (초기 데이터 포함)
- ✅ BeautifulSoup만으로 기본 데이터 추출 가능
- ✅ Cherokee보다 구조적으로 더 깔끔

**단점**:
- ⚠️ 일부 동적 필터링 (연도 선택 등)
- ⚠️ Playwright 선택적 필요 (과거 연도 접근)

### HTML 구조 (Phase 0에서 확인됨)

```html
<div id="agendaCenter">
  <div class="catAgendaRow">
    <strong>Dec 8, 2025</strong> — Posted Dec 4, 2025 9:44 AM
    <a href="/AgendaCenter/ViewFile/Agenda/_12082025-2854?html=true">
      Board of Lights and Water Meeting
    </a>
    <a href="/AgendaCenter/ViewFile/Minutes/_12082025-2854">
      <img src=".../HomeIconMinutes.png" />
    </a>

    <div class="downloads">
      <a href="/AgendaCenter/ViewFile/Agenda/_12082025-2854?html=true">HTML</a>
      <a href="/AgendaCenter/ViewFile/Agenda/_12082025-2854">PDF</a>
      <a href="/AgendaCenter/ViewFile/Agenda/_12082025-2854?packet=true">Packet</a>
    </div>
  </div>
</div>
```

### CSS Selectors (확인됨)

```python
SELECTORS = {
    "agenda_center": "#agendaCenter",
    "meeting_rows": ".catAgendaRow",
    "meeting_date": ".catAgendaRow strong",
    "meeting_title": ".catAgendaRow a[href*='ViewFile/Agenda']",
    "minutes_link": ".catAgendaRow a[href*='ViewFile/Minutes']",
    "html_download": "a[href*='?html=true']",
    "pdf_download": "a[href*='ViewFile/Agenda']:not([href*='?'])",
    "packet_download": "a[href*='?packet=true']",
}
```

### 날짜 형식

**표시 형식**: `"Dec 8, 2025"`
**URL 형식**: `_12082025` (MMDDYYYY)

**파싱 전략**:
- 표시 날짜: 자연어 파싱
- URL에서 추출: `_12082025` → `12/08/2025`

### 문서 링크 패턴

**패턴**: `/AgendaCenter/ViewFile/{type}/{dateID}-{documentID}?{params}`

**예시**:
- Agenda HTML: `/AgendaCenter/ViewFile/Agenda/_12082025-2854?html=true`
- Agenda PDF: `/AgendaCenter/ViewFile/Agenda/_12082025-2854`
- Packet: `/AgendaCenter/ViewFile/Agenda/_12082025-2854?packet=true`
- Minutes: `/AgendaCenter/ViewFile/Minutes/_12082025-2854`

---

## 🗓️ 구현 계획

### Phase 2.1: Marietta 스크래퍼 구현 (2-3시간)

#### 작업 항목

1. **MariettaScraper 클래스 생성** (1시간)
   - `src/scrapers/marietta.py`
   - BaseScraper 상속
   - HTML 가져오기 (httpx)
   - BeautifulSoup 파싱

2. **날짜 파싱 로직** (30분)
   - 자연어 날짜 → date 객체
   - 또는 URL에서 날짜 추출

3. **문서 링크 추출** (30분)
   - Agenda (HTML, PDF, Packet)
   - Minutes
   - URL 패턴 처리

4. **테스트** (30분)
   - 로컬 실행
   - 데이터 검증

#### 예상 코드

```python
# src/scrapers/marietta.py
class MariettaScraper(BaseScraper):
    BASE_URL = "https://www.mariettaga.gov"
    AGENDA_CENTER_URL = f"{BASE_URL}/AgendaCenter"

    SELECTORS = {
        "meeting_rows": ".catAgendaRow",
        # ...
    }

    def scrape(self, limit=None):
        # httpx로 HTML 가져오기
        # BeautifulSoup 파싱
        # Document 객체 생성
        pass

    def _parse_meeting_row(self, row):
        # 회의 행 파싱
        pass

    def _parse_date(self, date_text):
        # "Dec 8, 2025" → date(2025, 12, 8)
        pass
```

### Phase 2.2: CLI 통합 (30분)

#### 작업 항목

1. **CLI 명령어 업데이트**
   - `--jurisdiction` 선택지에 `marietta` 추가
   - 도움말 업데이트

2. **스크래퍼 팩토리 패턴** (선택)
   ```python
   def get_scraper(jurisdiction: Jurisdiction):
       if jurisdiction == Jurisdiction.CHEROKEE:
           return CherokeeScraper()
       elif jurisdiction == Jurisdiction.MARIETTA:
           return MariettaScraper()
       # ...
   ```

3. **테스트**
   ```bash
   python -m src.main backfill -j marietta -l 10
   ```

### Phase 2.3: 검증 및 문서화 (30분)

#### 작업 항목

1. **멀티 지자체 테스트**
   ```bash
   # Cherokee
   python -m src.main backfill -j cherokee -l 5

   # Marietta
   python -m src.main backfill -j marietta -l 5

   # 통계 확인
   python -m src.main stats
   ```

2. **문서 업데이트**
   - README.md: Marietta 추가
   - QUICKSTART.md: 예시 추가

---

## 📋 체크리스트

### 구현

- [ ] `src/scrapers/marietta.py` 생성
- [ ] MariettaScraper 클래스 구현
  - [ ] `get_base_url()` 메서드
  - [ ] `scrape()` 메서드
  - [ ] `_parse_meeting_row()` 메서드
  - [ ] `_parse_date()` 메서드
- [ ] CLI 업데이트
  - [ ] `marietta` 선택지 추가
  - [ ] 스크래퍼 팩토리 (선택)
- [ ] `__init__.py` 업데이트
  - [ ] MariettaScraper export

### 테스트

- [ ] **Marietta 단독 실행**
  ```bash
  python -m src.main backfill -j marietta -l 10
  ```
  - [ ] HTML 가져오기 성공
  - [ ] 파싱 성공
  - [ ] 날짜 파싱
  - [ ] 문서 링크 추출
  - [ ] DB 저장

- [ ] **멀티 지자체 테스트**
  - [ ] Cherokee 실행
  - [ ] Marietta 실행
  - [ ] 통계 확인 (2개 지자체)
  - [ ] 목록 조회

- [ ] **에러 처리**
  - [ ] 중복 데이터
  - [ ] 네트워크 오류
  - [ ] 잘못된 HTML

### 문서화

- [ ] README.md 업데이트
- [ ] QUICKSTART.md 예시 추가
- [ ] PHASE2-COMPLETE.md 작성

---

## 🎯 성공 지표

Phase 2는 다음 조건을 만족하면 완료:

1. [ ] Marietta 스크래퍼 완전 동작
2. [ ] 2개 지자체 모두 CLI에서 선택 가능
3. [ ] 데이터베이스에 두 지자체 데이터 공존
4. [ ] 통계에서 두 지자체 구분 표시
5. [ ] 중복 없이 안정적 실행

---

## ⏭️ Phase 3 Preview

Phase 2 완료 후:

1. **Alpharetta + Holly Springs** (CivicClerk SPA)
   - Playwright 통합
   - JavaScript 렌더링 처리
   - 코드 재사용 (동일 플랫폼)

2. **Continuous 모드**
   - 마지막 수집 이후 신규 문서만
   - 스케줄러 (선택)

3. **LLM 통합** (선택)
   - CSS Selector 자동 생성
   - 구조 변경 감지

---

## 📚 참고 자료

### Phase 0 분석

- `research/platform-analysis.md` - Marietta 상세 분석
- `research/websites-found.md` - Marietta 기본 정보

### Phase 1 구현

- `src/scrapers/base.py` - BaseScraper 참조
- `src/scrapers/cherokee.py` - 구현 패턴 참조

---

**작성일**: 2025-12-12
**Phase**: 2 (Expansion)
**예상 시간**: 3-4시간
**상태**: 🟡 시작
