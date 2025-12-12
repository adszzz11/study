# 지자체 웹사이트 조사 결과

> 4개 지자체의 회의 문서 웹사이트 URL 및 플랫폼 분석

**조사 날짜**: 2025-12-12

---

## ✅ 1. Cherokee County (비법인 지역)

### 기본 정보
- **공식 웹사이트**: https://www.cherokeecountyga.gov/
- **Planning & Zoning**: https://www.cherokeecountyga.gov/planning-and-zoning/

### 회의 문서 플랫폼
- **플랫폼**: Granicus
- **회의 포털**: https://cherokeega.granicus.com/ViewPublisher.php?view_id=1
- **문서 경로**: https://www.cherokeecountyga.gov/_focus/Meetings/Planning-Commission/

### 회의 일정
- **정기 회의**: 매월 첫째 화요일 오후 7시 (Public Hearing)
- **워크 세션**: 매월 셋째 월요일 오후 6:30시
- **장소**: County Administration Building (1130 Bluffs Parkway Canton, GA 30114)

### 문서 형식
- **Agendas**: PDF 형식 (예: `/agendas/20160202.pdf`)
- **Minutes**: Granicus 플랫폼에서 제공
- **Videos**: Granicus에서 스트리밍

### 기술적 특징
- ✅ Granicus 플랫폼 (표준 회의 관리 시스템)
- ✅ PDF 직접 링크
- ✅ Video 통합
- ⚠️ 검색 기능 있음 (Granicus 내장)

### 예상 난이도
- **스크래핑 난이도**: 🟡 중간
- **이유**: Granicus API 또는 HTML 파싱 필요

---

## ✅ 2. City of Holly Springs

### 기본 정보
- **공식 웹사이트**: https://www.hollyspringsga.us/
- **Agendas & Minutes**: https://www.hollyspringsga.us/129/Agendas-Minutes

### 회의 문서 플랫폼
- **플랫폼**: CivicClerk + IQM2
- **CivicClerk 포털**: https://hollyspringsga.portal.civicclerk.com/
- **IQM2 포털**: http://hollyspringsga.iqm2.com/citizens/default.aspx

### 문서 범위
- **City Council**: 회의록, 안건
- **Downtown Development Authority**: 문서 제공
- **Parks & Recreation Authority**: 문서 제공
- **Planning & Zoning Commission**: 문서 제공
- **Tree Commission**: 문서 제공

### 기간
- **현재 문서**: 2022년 8월 ~ 현재
- **과거 문서**: IQM2 포털에서 제공

### 기술적 특징
- ✅ CivicClerk (현대적 플랫폼)
- ✅ IQM2 (레거시 시스템)
- ⚠️ 두 개의 시스템 (통합 필요)
- 🔍 동적 렌더링 가능성

### 예상 난이도
- **스크래핑 난이도**: 🟡 중간
- **이유**: 두 개 플랫폼, 동적 렌더링 가능

---

## ✅ 3. City of Alpharetta

### 기본 정보
- **공식 웹사이트**: https://www.alpharetta.ga.us/
- **Planning Commission**: https://www.alpharetta.ga.us/423/Planning-Commission
- **City Meetings**: https://www.alpharetta.ga.us/523/City-Meetings

### 회의 문서 플랫폼
- **플랫폼**: CivicClerk
- **Meeting Portal**: https://alpharettaga.portal.civicclerk.com
- **Public Portal**: https://alpharettaga.civicclerk.com

### 회의 정보
- **Planning Commission**: Zoning 변경, 토지 이용 계획
- **City Council**: 정기 회의
- **장소**: Alpharetta City Hall (2 Park Plaza)

### 문서 제공
- **Agendas**: PDF
- **Minutes**: PDF
- **Videos**: YouTube 채널

### 기술적 특징
- ✅ CivicClerk (표준 플랫폼)
- ✅ 깔끔한 인터페이스
- ✅ YouTube 통합 (비디오)
- ⚠️ **JavaScript 기반 SPA** (2025-12-12 확인)
- ⚠️ **Playwright 필수** (정적 HTML 없음)
- 🟡 동적 렌더링 (초기 예상과 다름)

### 예상 난이도
- **스크래핑 난이도**: 🟡 중간 (수정됨)
- **이유**: JavaScript SPA로 Playwright 필수, 단 CivicClerk 표준 구조는 유지

### 검증 결과 (2025-12-12)

**테스트 방법**: WebFetch 도구로 페이지 접근
**결과**: `"You need to enable JavaScript to run this app."`

**의미**:
- CivicClerk 포털은 완전한 클라이언트 사이드 렌더링
- BeautifulSoup + httpx 조합으로는 데이터 추출 불가
- Playwright (또는 Selenium) **필수**

**기술 스택 영향**:
- ✅ Playwright 사용 확정
- ✅ 브라우저 자동화 필수
- ⚠️ 리소스 사용량 증가 (브라우저 실행)
- ⚠️ 실행 속도 감소 (렌더링 대기 시간)

---

## ✅ 4. City of Marietta

### 기본 정보
- **공식 웹사이트**: https://www.mariettaga.gov/
- **City Council**: https://www.mariettaga.gov/596/City-Council

### 회의 문서 플랫폼
- **플랫폼**: CivicEngage (Agenda Center)
- **Agenda Center**: https://www.mariettaga.gov/AgendaCenter
- **City Council Specific**: https://www.mariettaga.gov/AgendaCenter/City-Council-7

### 문서 제공
- **Agendas**: 회의 전 제공
- **Minutes**: 승인 후 제공
- **Videos**: https://www.mariettaga.gov/838/Council-Videos
- **Archived**: Document Center에서 과거 자료

### 관리
- **City Clerk's Office**: 모든 기록 유지
- **문서 종류**: Minutes, Ordinances, Resolutions, Contracts

### 기술적 특징
- ✅ CivicEngage (Agenda Center)
- ✅ Video 스트리밍
- ✅ Document Center (아카이브)
- 🔍 다양한 문서 타입

### 예상 난이도
- **스크래핑 난이도**: 🟡 중간
- **이유**: CivicEngage 구조 파악 필요

---

## 📊 비교 분석

### 플랫폼별 분류

| 지자체 | 플랫폼 | 표준화 | 문서 접근성 |
|--------|--------|--------|-------------|
| Cherokee County | Granicus | ✅ 높음 | 좋음 |
| Holly Springs | CivicClerk + IQM2 | ⚠️ 중간 | 보통 (이중 시스템) |
| Alpharetta | CivicClerk | ✅ 높음 | 매우 좋음 |
| Marietta | CivicEngage | ✅ 높음 | 좋음 |

### 난이도 평가

| 지자체 | 난이도 | 문서 타입 | 렌더링 | MVP 적합도 | 근거 |
|--------|--------|-----------|--------|------------|------|
| **Cherokee County** | 🟡 중간 | 4/4 | 동적? | ⭐⭐⭐ | Granicus 파싱 필요 |
| **Holly Springs** | 🟡 중간 | 4/4 | 동적 | ⭐⭐ | 이중 플랫폼 |
| **Alpharetta** | 🟡 중간 | 4/4 | **동적 ✅** | ⭐⭐⭐⭐ | CivicClerk SPA, Playwright 필수 |
| **Marietta** | 🟡 중간 | 4/4 | 동적? | ⭐⭐⭐ | CivicEngage 구조 |

---

## 🎯 MVP 지자체 추천

### 1순위: **City of Alpharetta** ⭐⭐⭐⭐ (수정됨)

**선정 이유**:
1. ✅ CivicClerk 플랫폼 (표준화)
2. ✅ 4가지 문서 타입 모두 제공
3. ✅ 좋은 문서화
4. ⚠️ **JavaScript SPA** (Playwright 필수)
5. ✅ 여전히 깔끔한 구조 예상

**근거**:
- CivicClerk는 많은 지자체가 사용하는 표준 플랫폼
- JavaScript 렌더링이지만 일관된 구조 예상
- Playwright 경험이 다른 지자체 확장에도 도움
- Holly Springs도 CivicClerk 사용 → 재사용 가능

**기술적 고려사항** (2025-12-12 업데이트):
- ⚠️ Playwright 필수 (정적 HTML 아님)
- ⚠️ 초기 예상보다 복잡도 증가
- ✅ 그러나 여전히 MVP 적합 (표준 플랫폼)
- ✅ 다른 지자체도 동적 렌더링 가능성 → 동일 기술 스택

### 2순위: Cherokee County ⭐⭐⭐

**이유**: Granicus 표준 플랫폼, 문서 완전성

### 3순위: Marietta ⭐⭐⭐

**이유**: CivicEngage 플랫폼, 좋은 아카이브

### 4순위: Holly Springs ⭐⭐

**이유**: 이중 플랫폼 (복잡도 증가)

---

## 🔧 기술 스택 확인

### 필요한 도구

| 플랫폼 | 접근 방법 | 필요 기술 |
|--------|-----------|-----------|
| **Granicus** | HTML 파싱 or API | BeautifulSoup or Playwright |
| **CivicClerk** | HTML 파싱 | BeautifulSoup (정적 가능성) |
| **IQM2** | HTML 파싱 | BeautifulSoup or Playwright |
| **CivicEngage** | HTML 파싱 | BeautifulSoup or Playwright |

### 권장 접근법

1. **MVP (Alpharetta)**:
   - BeautifulSoup로 시작
   - 필요시 Playwright 추가

2. **확장**:
   - Playwright 통합 (동적 사이트 대비)
   - 플랫폼별 어댑터 패턴

---

## 📋 다음 단계

### 즉시 실행 가능

1. ✅ **Alpharetta CivicClerk 구조 분석**
   - URL: https://alpharettaga.portal.civicclerk.com
   - HTML 구조 확인
   - CSS Selector 추출

2. ✅ **샘플 HTML 저장**
   - 각 플랫폼별 샘플 저장
   - 오프라인 테스트용

3. ✅ **LLM 테스트**
   - Alpharetta HTML → LLM 분석
   - Selector 생성 검증

### 향후 작업

4. ⏳ **나머지 3개 지자체 분석**
   - Granicus 구조 (Cherokee)
   - CivicEngage 구조 (Marietta)
   - IQM2 구조 (Holly Springs)

---

## 📚 Sources

**Cherokee County**:
- [Granicus Portal](https://cherokeega.granicus.com/ViewPublisher.php?view_id=1)
- [Planning & Zoning](https://www.cherokeecountyga.gov/planning-and-zoning/)

**Holly Springs**:
- [Agendas & Minutes](https://www.hollyspringsga.us/129/Agendas-Minutes)
- [CivicClerk Portal](https://hollyspringsga.portal.civicclerk.com/)
- [IQM2 Portal](http://hollyspringsga.iqm2.com/citizens/default.aspx)

**Alpharetta**:
- [CivicClerk Meeting Portal](https://alpharettaga.portal.civicclerk.com)
- [Planning Commission](https://www.alpharetta.ga.us/423/Planning-Commission)
- [City Meetings](https://www.alpharetta.ga.us/523/City-Meetings)

**Marietta**:
- [Agenda Center](https://www.mariettaga.gov/AgendaCenter)
- [City Council](https://www.mariettaga.gov/596/City-Council)
- [Council Videos](https://www.mariettaga.gov/838/Council-Videos)

---

**최종 업데이트**: 2025-12-12 (Alpharetta 초기 분석 완료)
**상태**: ✅ URL 발견 완료, 🔄 Alpharetta 구조 분석 중
**MVP 선정**: City of Alpharetta (CivicClerk SPA - Playwright 필수)

**Phase 0.2 진행 상황**:
- ✅ Alpharetta JavaScript 의존성 확인
- ✅ 분석 스크립트 생성 (`fetch_alpharetta_html.py`)
- ⏳ 로컬 실행 후 HTML 구조 분석 필요
- ⏳ CSS Selector 패턴 추출 대기
- ⏳ 나머지 3개 지자체 분석 대기
