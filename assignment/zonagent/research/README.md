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
2. 🔄 각 웹사이트 구조 분석
3. ⏳ 기술 스택 검증
4. ⏳ MVP 지자체 최종 선정

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

### 2. Alpharetta CivicClerk 분석 실행

```bash
# 스크립트 실행
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

## 📊 주요 발견사항

### Alpharetta CivicClerk

- **플랫폼**: CivicClerk (JavaScript SPA)
- **렌더링**: ⚠️ **동적 (Playwright 필수)**
- **평가**: ⭐⭐⭐⭐ (여전히 MVP 후보)

**중요**:
```
페이지 응답: "You need to enable JavaScript to run this app."
```

CivicClerk 포털은 완전한 JavaScript 기반이므로:
- BeautifulSoup 단독 사용 불가
- Playwright 또는 Selenium 필수
- 실제 구현에서도 동일한 접근 필요

### 기술적 영향

**확정된 기술 스택**:
- ✅ Playwright (동적 렌더링 필수)
- ✅ BeautifulSoup (HTML 파싱)
- ✅ Python 3.11+
- ✅ Anthropic Claude API

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
