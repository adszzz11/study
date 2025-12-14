# 플랫폼별 상세 분석 결과

> 4개 지자체의 렌더링 방식 및 기술적 특성 분석
> **분석 날짜**: 2025-12-12

---

## 📊 렌더링 방식 비교

| 지자체 | 플랫폼 | 렌더링 방식 | Playwright 필요 | 난이도 | MVP 적합도 |
|--------|--------|-------------|-----------------|--------|------------|
| **Cherokee County** | Granicus | 🟢 **서버 렌더링** | ❌ 불필요 | 🟢 **쉬움** | ⭐⭐⭐⭐⭐ |
| **Alpharetta** | CivicClerk | 🔴 **JavaScript SPA** | ✅ 필수 | 🟡 중간 | ⭐⭐⭐ |
| **Holly Springs** | CivicClerk + IQM2 | 🔴 **JavaScript SPA** | ✅ 필수 | 🟡 중간 | ⭐⭐ |
| **Marietta** | CivicEngage | 🟡 **하이브리드** (서버+jQuery) | ⚠️ 선택적 | 🟢 쉬움 | ⭐⭐⭐⭐ |

---

## ✅ 1. Cherokee County (Granicus) - 🟢 서버 렌더링

### 기본 정보
- **URL**: https://cherokeega.granicus.com/ViewPublisher.php?view_id=1
- **플랫폼**: Granicus (전통적 서버 렌더링)
- **렌더링**: ✅ **완전한 서버 렌더링**

### 렌더링 방식 ✅
```
상태: 서버에서 완전한 HTML 생성
메시지: 실제 데이터 포함된 테이블 즉시 표시
JavaScript: 선택적 (비디오 재생 등 부가 기능만)
```

**의미**:
- ✅ BeautifulSoup + httpx로 충분
- ✅ Playwright 불필요
- ✅ 가장 단순한 스크래핑
- ✅ 빠른 실행 속도

### HTML 구조 🎯

#### 테이블 구조
```html
<div id="granicus">
  <div class="archive">
    <table class="listingTable">
      <tr class="listHeader">
        <td>Name</td>
        <td>Date</td>
        <td>Agenda</td>
        <td>Minutes</td>
        <td>Video</td>
      </tr>
      <tr class="listingRow">
        <td class="listItem">Planning Commission Meeting</td>
        <td class="listItem">December 12, 2025 - 3:00 PM</td>
        <td class="listItem">
          <a href="AgendaViewer.php?view_id=1&event_id=12345">Agenda</a>
        </td>
        <td class="listItem">
          <a href="granicus.com/services/minutes/reports/...">Minutes PDF</a>
        </td>
        <td class="listItem">
          <a href="javascript:void(0)">Video</a>
        </td>
      </tr>
    </table>
  </div>
</div>
```

#### CSS Selectors (추출됨)
```python
CHEROKEE_SELECTORS = {
    "meeting_table": "table.listingTable",
    "header_row": "tr.listHeader",
    "meeting_rows": "tr.listingRow",
    "meeting_name": "td.listItem:nth-child(1)",
    "meeting_date": "td.listItem:nth-child(2)",
    "agenda_link": "td.listItem:nth-child(3) a",
    "minutes_link": "td.listItem:nth-child(4) a",
    "video_link": "td.listItem:nth-child(5) a",
}
```

### 날짜 형식 📅

**패턴**: `"Month DD, YYYY - H:MM AM/PM"`

**예시**:
- `"December 12, 2025 - 3:00 PM"`
- `"November 18, 2025 - 3:00 AM"`
- `"December  2, 2025 - 7:00 PM"` (주의: 일자 1자리 시 공백 2개)

**파싱 전략**:
```python
import re
from datetime import datetime

pattern = r"(\w+)\s+(\d{1,2}),\s+(\d{4})\s+-\s+(\d{1,2}):(\d{2})\s+(AM|PM)"
# 예: "December 12, 2025 - 3:00 PM"

match = re.match(pattern, date_string)
if match:
    month, day, year, hour, minute, ampm = match.groups()
    # datetime 객체 생성
```

### 문서 링크 패턴 🔗

#### 1. Agenda
- **패턴**: `AgendaViewer.php?view_id=1&event_id=[ID]`
- **타입**: HTML Viewer (Granicus 내장 뷰어)
- **추출**: `href` 속성에서 `event_id` 파라미터

#### 2. Minutes
- **패턴**: `granicus.com/services/minutes/reports/[...]`
- **타입**: PDF 직접 링크
- **추출**: `href` 속성 직접 사용

#### 3. Video
- **패턴**: `javascript:void(0)` (클라이언트 측 처리)
- **타입**: JavaScript 이벤트 핸들러
- **추출**: ⚠️ 복잡 (Playwright 필요할 수도)

### 페이지네이션 📄

**방식**: ❌ **페이지네이션 없음**

**구조**:
- 연도별 섹션으로 분류 (2025, 2024, 2023, ...)
- 전체 데이터 한 페이지에 표시
- 스크롤로 이동

**스크래핑 전략**:
- 단일 페이지 파싱으로 모든 데이터 획득 가능
- 연도별 섹션 구분 필요 없음 (모든 행 동일 구조)

### 기술적 특징 ⚙️

**장점**:
- ✅ 완전한 서버 렌더링
- ✅ 일관된 테이블 구조
- ✅ 명확한 CSS 클래스
- ✅ BeautifulSoup만으로 충분
- ✅ 빠른 스크래핑 속도
- ✅ 낮은 리소스 사용량

**단점**:
- ⚠️ 비디오 링크는 JavaScript 처리
- ⚠️ 날짜 파싱 시 공백 처리 필요

### MVP 적합성 평가 🎯

**난이도**: 🟢 **쉬움** (4개 중 가장 쉬움!)

**점수**: ⭐⭐⭐⭐⭐

**근거**:
1. ✅ 서버 렌더링 (Playwright 불필요)
2. ✅ 단순한 테이블 구조
3. ✅ 명확한 Selector
4. ✅ 페이지네이션 없음
5. ✅ 빠른 개발 가능

**예상 개발 시간**:
- HTML 파싱: 2-3시간
- 데이터 추출: 1-2시간
- 테스트: 1시간
- **총 4-6시간** (가장 빠름)

---

## 🔴 2. Alpharetta (CivicClerk) - JavaScript SPA

### 기본 정보
- **URL**: https://alpharettaga.portal.civicclerk.com
- **플랫폼**: CivicClerk (Modern SPA)
- **렌더링**: 🔴 **JavaScript 기반 SPA**

### 렌더링 방식 ❌
```
상태: 클라이언트 측 렌더링
메시지: "You need to enable JavaScript to run this app."
JavaScript: 필수 (모든 데이터 렌더링)
```

**의미**:
- ❌ BeautifulSoup 단독 불가
- ✅ Playwright 필수
- ⚠️ 브라우저 자동화 필요
- ⚠️ 느린 실행 속도

### HTML 구조 🎯

**초기 HTML**:
```html
<div id="root">
  <div>You need to enable JavaScript to run this app.</div>
</div>
```

**렌더링 후 구조**: ⏳ 로컬 실행 필요 (`fetch_alpharetta_html.py`)

### 기술적 특징 ⚙️

**장점**:
- ✅ CivicClerk 표준 플랫폼
- ✅ 깔끔한 인터페이스 (예상)
- ✅ Holly Springs도 동일 플랫폼 → 코드 재사용

**단점**:
- ❌ Playwright 필수
- ⚠️ 느린 실행 속도
- ⚠️ 리소스 사용량 증가
- ⚠️ 복잡한 디버깅

### MVP 적합성 평가 🎯

**난이도**: 🟡 중간

**점수**: ⭐⭐⭐

**근거**:
1. ❌ Playwright 필수
2. ⚠️ 복잡도 증가
3. ✅ 하지만 표준 플랫폼
4. ✅ 코드 재사용 가능 (Holly Springs)

**예상 개발 시간**:
- Playwright 설정: 2-3시간
- HTML 구조 분석: 2-3시간
- 데이터 추출: 3-4시간
- 테스트: 2시간
- **총 9-12시간**

---

## 🔴 3. Holly Springs (CivicClerk + IQM2) - JavaScript SPA

### 기본 정보
- **주 플랫폼**: https://hollyspringsga.portal.civicclerk.com/
- **레거시**: http://hollyspringsga.iqm2.com/citizens/default.aspx
- **렌더링**: 🔴 **JavaScript SPA** (Alpharetta와 동일)

### 렌더링 방식 ❌

**CivicClerk 포털**: Alpharetta와 동일 (JavaScript SPA)
```
"You need to enable JavaScript to run this app."
```

**IQM2 포털**: ⏳ 별도 분석 필요

### 기술적 특징 ⚙️

**장점**:
- ✅ Alpharetta와 동일 플랫폼 → **코드 100% 재사용**
- ✅ 한 번 구현하면 두 지자체 커버

**단점**:
- ❌ Playwright 필수
- ⚠️ **이중 플랫폼** (CivicClerk + IQM2)
- ⚠️ 레거시 시스템 처리 필요
- ⚠️ 복잡도 가장 높음

### MVP 적합성 평가 🎯

**난이도**: 🟡 중간~어려움

**점수**: ⭐⭐

**근거**:
1. ✅ Alpharetta 코드 재사용
2. ❌ 이중 플랫폼 (복잡도 증가)
3. ❌ MVP에는 부적합
4. ✅ Phase 2 확장 단계에서 추가

**예상 개발 시간**:
- CivicClerk: Alpharetta 재사용 (1-2시간)
- IQM2 분석: 3-4시간
- 통합: 2-3시간
- 테스트: 2시간
- **총 8-11시간**

---

## 🟡 4. Marietta (CivicEngage) - 서버+jQuery 하이브리드

### 기본 정보
- **URL**: https://www.mariettaga.gov/AgendaCenter
- **플랫폼**: CivicEngage (Agenda Center)
- **렌더링**: 🟡 **하이브리드** (서버 렌더링 + jQuery 동적 기능)

### 렌더링 방식 ✅

**초기 로드**: ✅ 서버에서 완전한 HTML 생성
**동적 기능**: jQuery를 통한 AJAX (선택적)

```html
<!-- 실제 데이터 포함된 HTML -->
<div id="agendaCenter">
  <div class="catAgendaRow">
    <strong>Dec 8, 2025</strong> — Posted Dec 4, 2025 9:44 AM
    <a href="/AgendaCenter/ViewFile/Agenda/_12082025-2854?html=true">
      Board of Lights and Water Meeting
    </a>
    <a href="/AgendaCenter/ViewFile/Minutes/_12082025-2854">
      <img src="/Areas/AgendaCenter/Assets/Images/HomeIconMinutes.png" />
    </a>

    <div class="downloads">
      <a href="/AgendaCenter/ViewFile/Agenda/_12082025-2854?html=true">HTML</a>
      <a href="/AgendaCenter/ViewFile/Agenda/_12082025-2854">PDF</a>
      <a href="/AgendaCenter/ViewFile/Agenda/_12082025-2854?packet=true">Packet</a>
    </div>
  </div>
</div>
```

**의미**:
- ✅ BeautifulSoup로 기본 데이터 추출 가능
- ⚠️ 일부 동적 필터링은 Playwright 필요할 수도
- ✅ 대부분 정적 HTML로 충분

### HTML 구조 🎯

#### CSS Selectors (추출됨)
```python
MARIETTA_SELECTORS = {
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

### 날짜 형식 📅

**표시 형식**: `"Dec 8, 2025"` (자연어)
**내부 형식**: `MM/DD/YYYY` (URL 파라미터에서)

**예시**:
```
표시: "Dec 8, 2025"
URL: /AgendaCenter/ViewFile/Agenda/_12082025-2854
날짜 추출: 12/08/2025 (URL의 _12082025 파싱)
```

### 문서 링크 패턴 🔗

**패턴**: `/AgendaCenter/ViewFile/{type}/{dateID}-{documentID}?{params}`

#### 1. Agenda
- HTML: `?html=true`
- PDF: 파라미터 없음
- Packet: `?packet=true`

#### 2. Minutes
- `/AgendaCenter/ViewFile/Minutes/_12082025-2854`

**예시**:
```python
# URL 파싱
url = "/AgendaCenter/ViewFile/Agenda/_12082025-2854"
doc_type = "Agenda"  # URL path에서 추출
date_id = "12082025"  # _12082025 파싱
doc_id = "2854"
```

### 동적 기능 ⚙️

**JavaScript 필터링**:
```javascript
// 연도 변경
javascript:changeYear(2025, 9, 'a0')

// AJAX 카테고리 업데이트
'/AgendaCenter/UpdateCategoryList'
```

**스크래핑 전략**:
- ✅ 기본 목록: BeautifulSoup만으로 충분
- ⚠️ 과거 연도 데이터: Playwright로 JavaScript 필터 조작 필요

### MVP 적합성 평가 🎯

**난이도**: 🟢 쉬움~중간

**점수**: ⭐⭐⭐⭐

**근거**:
1. ✅ 서버 렌더링 (대부분)
2. ✅ 명확한 HTML 구조
3. ⚠️ 일부 동적 기능
4. ✅ BeautifulSoup 우선, Playwright 선택적

**예상 개발 시간**:
- HTML 파싱: 2-3시간
- 데이터 추출: 2-3시간
- 동적 필터링 (선택): 2-3시간
- 테스트: 1-2시간
- **총 7-11시간**

---

## 🏆 MVP 지자체 재평가

### 순위 변경 ⚡

| 순위 | 지자체 | 플랫폼 | 렌더링 | 난이도 | 점수 | 예상 시간 |
|------|--------|--------|--------|--------|------|-----------|
| **1위** 🥇 | **Cherokee County** | Granicus | 서버 | 🟢 | ⭐⭐⭐⭐⭐ | **4-6시간** |
| **2위** 🥈 | **Marietta** | CivicEngage | 하이브리드 | 🟢 | ⭐⭐⭐⭐ | 7-11시간 |
| **3위** 🥉 | **Alpharetta** | CivicClerk | SPA | 🟡 | ⭐⭐⭐ | 9-12시간 |
| 4위 | Holly Springs | CivicClerk+IQM2 | SPA | 🟡 | ⭐⭐ | 8-11시간 |

### 새로운 MVP 추천: Cherokee County 🎯

**이유**:
1. ✅ **완전한 서버 렌더링** (Playwright 불필요)
2. ✅ **가장 단순한 구조** (테이블)
3. ✅ **가장 빠른 개발** (4-6시간)
4. ✅ **낮은 리소스 사용**
5. ✅ **검증된 기술** (BeautifulSoup)

**Alpharetta 대신 Cherokee를 선택하는 이유**:
- Alpharetta는 Playwright 필수 → 복잡도 증가
- Cherokee는 BeautifulSoup만으로 충분 → MVP 철학에 부합
- 개발 시간 50% 단축 (9-12시간 → 4-6시간)
- 기술 검증 먼저, 복잡한 기술은 Phase 2에서

**Phase별 전략**:
- **Phase 1 (MVP)**: Cherokee County (서버 렌더링, 단순)
- **Phase 2 (확장)**: Marietta 추가 (하이브리드)
- **Phase 3 (완성)**: Alpharetta + Holly Springs (SPA, 코드 재사용)

---

## 📋 다음 단계

### 즉시 실행

1. ✅ **Cherokee County 스크립트 생성**
   - BeautifulSoup 기반
   - `fetch_cherokee_html.py`
   - Selector 검증

2. ⏳ Marietta 스크립트 생성 (선택)
   - BeautifulSoup 우선
   - 동적 기능은 나중에

3. ⏳ MVP 최종 확정
   - Cherokee County로 변경
   - 구현 계획 업데이트

### 로컬 실행 (병렬)

- Alpharetta: `fetch_alpharetta_html.py` (이미 생성됨)
- Cherokee: 새 스크립트 생성 후 실행

---

**최종 업데이트**: 2025-12-12 (플랫폼 분석 완료)
**MVP 추천**: Cherokee County (Granicus) ← **변경됨**
**근거**: 서버 렌더링, 가장 단순, 가장 빠른 개발
