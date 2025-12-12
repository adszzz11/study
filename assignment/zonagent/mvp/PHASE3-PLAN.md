# Phase 3 실행 계획

> **날짜**: 2025-12-12
> **Phase**: 3 (Completion - 4개 지자체 완성)
> **목표**: Alpharetta + Holly Springs 추가 (CivicClerk SPA)

---

## 📌 Executive Summary

Phase 3에서는 **Alpharetta**와 **Holly Springs**를 추가하여 **4개 지자체 완전 지원**을 달성합니다.

**핵심 도전 과제**:
- 🔴 **JavaScript SPA 렌더링**: Playwright 필수
- ✅ **코드 재사용**: 두 지자체 모두 CivicClerk 플랫폼

**예상 시간**:
- Playwright 통합: 1-2시간
- Alpharetta 구현: 2-3시간
- Holly Springs 구현: 1시간 (코드 재사용)
- 통합 테스트: 1시간
- **총 5-7시간**

---

## 🎯 Phase 3 목표

### 구현할 기능

1. **Playwright 통합** ✨
   - 브라우저 자동화 설정
   - JavaScript 렌더링 대기
   - 효율적인 페이지 로딩 전략

2. **AlpharettaScraper** ✨
   - CivicClerk SPA 파싱
   - 동적 렌더링 처리
   - 회의 목록 추출
   - Agenda, Minutes 수집

3. **HollySpringScraper** ✨
   - Alpharetta 코드 재사용
   - URL만 변경
   - CivicClerk 공통 로직 활용

4. **멀티 플랫폼 아키텍처** ♻️
   - BaseScraper 확장
   - Playwright vs BeautifulSoup 분기
   - 스크래퍼 팩토리 확장

5. **4개 지자체 통합** 🔧
   - CLI 업데이트
   - 전체 통계 조회
   - 통합 테스트

---

## 🏗️ 기술 스택 추가

### 새로운 의존성

```python
# requirements.txt 추가
playwright==1.41.0       # 브라우저 자동화
```

### 설치 및 설정

```bash
# Playwright 설치
pip install playwright

# Chromium 브라우저 설치
playwright install chromium
```

---

## 📋 CivicClerk 플랫폼 분석

### Alpharetta

**URL**: https://alpharettaga.portal.civicclerk.com

**렌더링 방식**: 🔴 JavaScript SPA
- 초기 HTML: `<div id="root">You need to enable JavaScript...</div>`
- Playwright 필수
- 비동기 데이터 로딩

**예상 HTML 구조** (렌더링 후):
```html
<div id="root">
  <div class="meeting-list">
    <div class="meeting-item">
      <div class="meeting-date">December 12, 2025</div>
      <div class="meeting-title">City Council Meeting</div>
      <div class="meeting-documents">
        <a href="/documents/agenda-123.pdf">Agenda</a>
        <a href="/documents/minutes-123.pdf">Minutes</a>
      </div>
    </div>
  </div>
</div>
```

**파싱 전략**:
1. Playwright로 페이지 로드
2. JavaScript 렌더링 완료 대기
3. 렌더링된 HTML 추출
4. BeautifulSoup로 파싱

### Holly Springs

**URL**: https://hollyspringsga.portal.civicclerk.com/

**특징**: Alpharetta와 **100% 동일 플랫폼**

**코드 재사용**:
```python
class HollySpringScraper(AlpharettaScraper):
    """Holly Springs - Alpharetta 코드 완전 재사용"""

    JURISDICTION = Jurisdiction.HOLLY_SPRINGS
    BASE_URL = "https://hollyspringsga.portal.civicclerk.com/"

    # 나머지 로직 모두 상속
```

---

## 🔧 구현 단계

### Step 1: Playwright 통합 (1-2h)

**파일**: `src/utils.py` 또는 `src/scrapers/playwright_scraper.py`

**작업**:
1. Playwright 초기화 함수
2. 페이지 로드 및 렌더링 대기
3. HTML 추출 헬퍼 함수
4. 에러 처리

**코드 스케치**:
```python
# src/scrapers/playwright_scraper.py
from playwright.sync_api import sync_playwright
from .base import BaseScraper

class PlaywrightScraper(BaseScraper):
    """Playwright 기반 스크래퍼 베이스 클래스"""

    def fetch_html(self, url: str, wait_for: str = None) -> str:
        """Playwright로 HTML 가져오기"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 페이지 로드
            page.goto(url, wait_until="networkidle")

            # 선택적 대기
            if wait_for:
                page.wait_for_selector(wait_for, timeout=10000)

            # HTML 추출
            html = page.content()

            browser.close()
            return html
```

### Step 2: AlpharettaScraper 구현 (2-3h)

**파일**: `src/scrapers/alpharetta.py`

**작업**:
1. PlaywrightScraper 상속
2. CivicClerk HTML 구조 분석
3. CSS Selector 추출
4. 날짜 파싱
5. 문서 타입 판별

**구현 체크리스트**:
- [ ] PlaywrightScraper 상속
- [ ] get_base_url() 구현
- [ ] scrape() 메서드 구현
- [ ] HTML 렌더링 대기 로직
- [ ] 회의 목록 파싱
- [ ] Agenda, Minutes 링크 추출
- [ ] 날짜 파싱
- [ ] 로깅 추가

### Step 3: HollySpringScraper 구현 (1h)

**파일**: `src/scrapers/holly_springs.py`

**작업**:
1. AlpharettaScraper 상속
2. URL 오버라이드
3. Jurisdiction 변경
4. 필요 시 Selector 조정

**구현**:
```python
# src/scrapers/holly_springs.py
from .alpharetta import AlpharettaScraper
from ..models import Jurisdiction

class HollySpringScraper(AlpharettaScraper):
    """Holly Springs - CivicClerk 플랫폼"""

    JURISDICTION = Jurisdiction.HOLLY_SPRINGS
    BASE_URL = "https://hollyspringsga.portal.civicclerk.com/"

    # 필요시 SELECTORS 오버라이드
    # 대부분 Alpharetta와 동일
```

### Step 4: 스크래퍼 팩토리 확장 (30분)

**파일**: `src/scrapers/__init__.py`

**작업**:
```python
from .cherokee import CherokeeScraper
from .marietta import MariettaScraper
from .alpharetta import AlpharettaScraper
from .holly_springs import HollySpringScraper

def get_scraper(jurisdiction_name: str):
    """스크래퍼 팩토리 함수"""
    scrapers = {
        "cherokee": CherokeeScraper,
        "marietta": MariettaScraper,
        "alpharetta": AlpharettaScraper,       # 추가
        "holly_springs": HollySpringScraper,   # 추가
    }

    scraper_class = scrapers.get(jurisdiction_name.lower())
    if not scraper_class:
        raise ValueError(
            f"Unsupported jurisdiction: {jurisdiction_name}. "
            f"Available: {', '.join(scrapers.keys())}"
        )

    return scraper_class()
```

### Step 5: CLI 업데이트 (30분)

**파일**: `src/main.py`

**작업**:
1. jurisdiction 선택지 추가
2. 표시 이름 매핑
3. 도움말 업데이트

**변경**:
```python
# src/main.py

# 지자체 이름 매핑
jurisdiction_names = {
    "cherokee": "Cherokee County",
    "marietta": "City of Marietta",
    "alpharetta": "City of Alpharetta",       # 추가
    "holly_springs": "City of Holly Springs", # 추가
}

# argparse choices
choices=["cherokee", "marietta", "alpharetta", "holly_springs"]
```

### Step 6: 통합 테스트 (1h)

**테스트 시나리오**:

1. **개별 실행**:
   ```bash
   python -m src.main backfill -j alpharetta -l 5
   python -m src.main backfill -j holly_springs -l 5
   ```

2. **4개 지자체 전체 실행**:
   ```bash
   python -m src.main backfill -j cherokee -l 5
   python -m src.main backfill -j marietta -l 5
   python -m src.main backfill -j alpharetta -l 5
   python -m src.main backfill -j holly_springs -l 5
   ```

3. **통계 확인**:
   ```bash
   python -m src.main stats
   ```

4. **문서 목록**:
   ```bash
   python -m src.main list -l 50
   ```

---

## 📊 예상 결과

### 데이터 수집 예상

| 지자체 | 예상 회의 수 | 예상 문서 수 | 소요 시간 | 플랫폼 |
|--------|------------|------------|----------|--------|
| Cherokee | ~15 | ~40 | ~3초 | Granicus |
| Marietta | ~20 | ~60 | ~3초 | CivicEngage |
| Alpharetta | ~25 | ~50 | ~10초 | CivicClerk |
| Holly Springs | ~15 | ~30 | ~10초 | CivicClerk |
| **총계** | ~75 | ~180 | ~26초 | - |

**참고**: Playwright는 브라우저 실행으로 인해 BeautifulSoup보다 3-5배 느림

### 데이터베이스 크기

- 예상 DB 크기: ~200KB
- 문서 평균 크기: ~1KB

---

## 🚧 예상 문제 및 해결책

### 문제 1: Playwright 느린 속도

**원인**: 브라우저 실행 오버헤드

**해결책**:
1. 브라우저 재사용 (컨텍스트 캐싱)
2. Headless 모드 사용
3. 불필요한 리소스 차단 (이미지, 폰트 등)

### 문제 2: CivicClerk HTML 구조 불명확

**원인**: 로컬에서 렌더링 전까지 구조 확인 불가

**해결책**:
1. 먼저 Playwright로 HTML 추출
2. HTML 파일로 저장하여 분석
3. CSS Selector 수동 추출
4. 스크래퍼 구현

### 문제 3: 렌더링 타이밍

**원인**: JavaScript 비동기 데이터 로딩

**해결책**:
1. `wait_for_selector()` 사용
2. `networkidle` 이벤트 대기
3. 특정 요소 출현 대기

---

## 📁 생성/수정할 파일

### 새로 생성 (4개)

```
mvp/src/scrapers/
├── playwright_scraper.py  # Playwright 베이스 클래스 (~150 라인)
├── alpharetta.py          # Alpharetta 스크래퍼 (~250 라인)
├── holly_springs.py       # Holly Springs 스크래퍼 (~50 라인)
└── PHASE3-PLAN.md         # 이 파일
```

### 수정 (3개)

```
mvp/
├── src/scrapers/__init__.py   # alpharetta, holly_springs 추가
├── src/main.py                # CLI 선택지 추가
└── requirements.txt           # playwright 추가
```

### 문서화 (예정)

```
mvp/
├── PHASE3-COMPLETE.md     # Phase 3 완료 보고서
└── README.md              # 4개 지자체 정보 업데이트
```

---

## ⏱️ 예상 시간

| 단계 | 작업 | 시간 |
|------|------|------|
| 1 | Playwright 통합 | 1-2시간 |
| 2 | AlpharettaScraper | 2-3시간 |
| 3 | HollySpringScraper | 1시간 |
| 4 | 팩토리/CLI 업데이트 | 1시간 |
| 5 | 통합 테스트 | 1시간 |
| 6 | 문서화 | 1시간 |
| **총계** | | **7-10시간** |

**예상 vs Phase 1-2**:
- Phase 1 (Cherokee): 3시간 (예상 6h)
- Phase 2 (Marietta): 2시간 (예상 4h)
- Phase 3 (Alpharetta + Holly Springs): 7-10시간 (예상 9-12h)
- **패턴**: 구현 속도 일관되게 빠름

---

## 🎯 체크리스트

### 구현 전 준비

- [ ] Phase 2 로컬 테스트 완료 (선택적)
- [ ] Playwright 설치 및 테스트
- [ ] Alpharetta HTML 구조 확인
- [ ] Holly Springs HTML 구조 확인

### 구현

- [ ] PlaywrightScraper 베이스 클래스
- [ ] AlpharettaScraper 구현
- [ ] HollySpringScraper 구현
- [ ] 스크래퍼 팩토리 확장
- [ ] CLI 업데이트
- [ ] requirements.txt 업데이트

### 테스트

- [ ] Alpharetta 단독 실행
- [ ] Holly Springs 단독 실행
- [ ] 4개 지자체 전체 실행
- [ ] 통계 조회
- [ ] 에러 처리 테스트

### 문서화

- [ ] PHASE3-COMPLETE.md
- [ ] README.md 업데이트
- [ ] FINAL-SUMMARY.md 업데이트

---

## 🚀 Phase 3 완료 후

### 달성 목표

- ✅ **4개 지자체 완전 지원**
- ✅ **3개 플랫폼 지원** (Granicus, CivicEngage, CivicClerk)
- ✅ **2가지 렌더링 방식** (서버, JavaScript SPA)
- ✅ **확장 가능한 아키텍처**

### 다음 단계 (Phase 4 - 선택적)

1. **Continuous 모드** (1-2일)
   - 새 문서만 수집
   - 스케줄러 통합 (cron)
   - 증분 업데이트

2. **LLM 통합** (2-3일)
   - CSS Selector 자동 추출
   - 에러 자동 복구
   - Agentic 문서 분석

3. **문서 다운로드** (1일)
   - PDF 로컬 저장
   - 체크섬 검증
   - 중복 방지

4. **PostgreSQL 마이그레이션** (1일)
   - 프로덕션 DB 전환
   - 마이그레이션 스크립트
   - 성능 최적화

---

**생성일**: 2025-12-12
**Phase**: 3 (Completion)
**상태**: 계획 완료, 구현 시작 대기
**다음**: Playwright 설치 및 HTML 구조 확인
