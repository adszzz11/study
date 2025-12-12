# Phase 0 Research

> 4개 지자체 웹사이트 구조 분석 및 기술 검증

## 📂 디렉터리 구조

```
research/
├── README.md                    # 이 파일
├── phase0-progress.md           # 진행 상황 추적
├── websites-found.md            # 발견한 웹사이트 URL 및 분석
├── fetch_alpharetta_html.py     # Alpharetta HTML 구조 분석 스크립트
├── requirements.txt             # 의존성 패키지
└── html_samples/                # 저장된 HTML 샘플 (생성됨)
    ├── alpharetta_portal_*.html
    ├── alpharetta_portal_*.png
    └── sample_meeting_item_*.html
```

## 🎯 Phase 0 목표

1. ✅ 4개 지자체 웹사이트 URL 확인
2. ✅ 각 웹사이트 렌더링 방식 분석
3. ✅ 플랫폼별 특성 파악
4. ✅ MVP 지자체 최종 선정 → **Cherokee County** 🥇

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 연구 디렉터리로 이동
cd /Users/leetangle/code/Note/assignment/zonagent/research

# 가상환경 생성 (선택사항, 권장)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# Playwright 브라우저 설치
playwright install chromium
```

### 2A. Cherokee County 분석 실행 (우선순위 1 🥇)

```bash
# 스크립트 실행 (Playwright 불필요!)
python fetch_cherokee_html.py
```

**특징**:
- ✅ httpx + BeautifulSoup만 사용 (간단!)
- ✅ Playwright 설치 불필요
- ✅ 빠른 실행 (~5초)
- ✅ 낮은 리소스 사용

**출력 예시**:
```
============================================================
Cherokee County Granicus HTML 구조 분석 도구
============================================================
📡 페이지 가져오기: https://cherokeega.granicus.com/...
✅ HTML 수신 완료
   상태 코드: 200
   파일 크기: 123,456 bytes
✅ HTML 저장: html_samples/cherokee_granicus_20251212_143025.html

🔍 HTML 구조 분석:
✅ 회의 테이블 발견: <table class='listingTable'>
✅ 테이블 헤더: ['Name', 'Date', 'Agenda', 'Minutes', 'Video']
✅ 회의 행 발견: 48개

📋 첫 번째 회의 상세 분석:
  이름: Planning Commission Meeting
  날짜: December 12, 2025 - 3:00 PM
  Agenda: AgendaViewer.php?view_id=1&event_id=12345
  Minutes: .../minutes/reports/...
  Video: javascript:void(0)

🎯 CSS Selector 검증:
  ✅ meeting_table      : table.listingTable                      → 1개
  ✅ meeting_rows       : tr.listingRow                           → 48개
  ✅ meeting_date       : td.listItem:nth-child(2)                → 48개

📅 날짜 형식 분석:
  ✅ 날짜 패턴 매칭: 5/5
  예시: December 12, 2025 - 3:00 PM

✅ 분석 완료!
```

### 2B. Alpharetta CivicClerk 분석 실행 (참고용)

```bash
# 스크립트 실행 (Playwright 필요)
python fetch_alpharetta_html.py
```

**출력 예시**:
```
============================================================
Alpharetta CivicClerk HTML 구조 분석 도구
============================================================
🚀 Playwright 시작...
📡 페이지 로딩: https://alpharettaga.portal.civicclerk.com
⏳ JavaScript 렌더링 대기...
✅ HTML 저장 완료: html_samples/alpharetta_portal_20251212_143025.html
   파일 크기: 234,567 bytes
📸 스크린샷 저장: html_samples/alpharetta_portal_20251212_143025.png

🔍 페이지 구조 분석:
  ✅ 'table.meeting-list tr': 25개 발견
     샘플 저장: html_samples/sample_meeting_item_20251212_143025.html

🔗 문서 링크 분석:
  문서 관련 링크: 48개
    1. Agenda                                                  -> /meetings/agenda/123
    2. Minutes                                                 -> /meetings/minutes/123
    ...
```

### 3. 결과 확인

```bash
# HTML 샘플 확인
ls -lh html_samples/

# 최신 HTML 파일 보기 (처음 100줄)
head -n 100 html_samples/alpharetta_portal_*.html | less

# 스크린샷 확인 (macOS)
open html_samples/alpharetta_portal_*.png
```

## 📊 주요 발견사항 및 MVP 선정

### 🥇 MVP: Cherokee County (Granicus)

- **플랫폼**: Granicus (서버 렌더링)
- **렌더링**: ✅ **정적 HTML** (Playwright 불필요!)
- **평가**: ⭐⭐⭐⭐⭐ **최고 점수**

**중요 장점**:
- ✅ **완전한 서버 렌더링** → BeautifulSoup만으로 충분
- ✅ **단순한 테이블 구조** → CSS Selector 명확
- ✅ **빠른 개발 가능** → 예상 4-6시간 (50% 단축)
- ✅ **낮은 리소스 사용** → 브라우저 자동화 불필요

**기술 스택**:
- httpx (HTTP 요청)
- BeautifulSoup (HTML 파싱)
- Python 3.11+

### 🥈 2순위: Marietta (CivicEngage)

- **플랫폼**: CivicEngage (서버 + jQuery 하이브리드)
- **렌더링**: ✅ 대부분 서버, 일부 동적
- **평가**: ⭐⭐⭐⭐

### 🥉 3순위: Alpharetta (CivicClerk)

- **플랫폼**: CivicClerk (JavaScript SPA)
- **렌더링**: ⚠️ **동적 (Playwright 필수)**
- **평가**: ⭐⭐⭐

**주의**:
```
페이지 응답: "You need to enable JavaScript to run this app."
```

CivicClerk 포털은 JavaScript 기반이므로:
- BeautifulSoup 단독 사용 불가
- Playwright 필수
- Phase 2 이후 추가 예정

### 기술 스택 최종 결정

**MVP (Phase 1) - Cherokee County**:
- ✅ httpx (HTTP 요청)
- ✅ BeautifulSoup (HTML 파싱)
- ✅ Python 3.11+
- ✅ Anthropic Claude API (LLM 기능)

**Phase 2 이후 - 동적 사이트**:
- Playwright 추가 (Alpharetta, Holly Springs용)

## 📝 문서

### phase0-progress.md
- Phase 0 진행 상황 상세 추적
- 각 지자체별 조사 체크리스트
- 기술 검증 단계

### websites-found.md
- 4개 지자체 웹사이트 URL
- 플랫폼별 분류 (Granicus, CivicClerk, IQM2, CivicEngage)
- 난이도 평가 및 MVP 추천

## 🔧 다음 단계

### 즉시 실행 가능
1. ✅ `fetch_alpharetta_html.py` 실행
2. ⏳ 저장된 HTML 구조 분석
3. ⏳ CSS Selector 패턴 추출
4. ⏳ LLM 테스트 (HTML → Selectors 생성)

### 이후 작업
5. ⏳ Cherokee County (Granicus) 분석
6. ⏳ Holly Springs (CivicClerk + IQM2) 분석
7. ⏳ Marietta (CivicEngage) 분석
8. ⏳ MVP 지자체 최종 확정

## ⚠️ 주의사항

### API 사용량
- LLM 테스트 시 비용 발생 (예상: ~$0.001/요청)
- Anthropic API Key 필요 (`ANTHROPIC_API_KEY` 환경변수)

### 브라우저 리소스
- Playwright는 실제 Chromium 브라우저 실행
- 메모리: ~200-500MB per instance
- 너무 많은 동시 실행 지양

## 📚 참고 자료

**생성된 도구**:
- `fetch_alpharetta_html.py`: 메인 분석 스크립트
- `requirements.txt`: Python 패키지 목록

**분석 문서**:
- `phase0-progress.md`: 진행 상황
- `websites-found.md`: 발견 결과

**관련 파일**:
- `../implementation-plan/detailed-design.md`: 구현 설계
- `../IMPLEMENTATION-MASTER.md`: 전체 계획

---

**최종 업데이트**: 2025-12-12
**현재 단계**: Phase 0.2 - Alpharetta 구조 분석 중
