# Phase 0 진행 상황

> 사전 조사 및 기술 검증 진행 기록

## 🎯 목표

1. ✅ 4개 지자체 웹사이트 URL 확인
2. ⏳ 각 웹사이트 구조 분석
3. ⏳ 기술 스택 검증
4. ⏳ MVP 지자체 선정

---

## 📍 Step 1: 웹사이트 URL 찾기

### 검색 전략

각 지자체에 대해 다음 키워드로 검색:
```
"[지자체명] Georgia planning zoning meetings"
"[지자체명] meeting minutes agendas"
"[지자체명] planning commission"
```

---

### 1.1 Cherokee County (비법인 지역)

**검색 키워드**:
- "Cherokee County Georgia planning commission meetings"
- "Cherokee County Georgia zoning meetings"

**예상 사이트**:
- 공식 웹사이트: https://www.cherokeega.com/
- 회의 정보 경로: /government/departments/planning-zoning/

**조사 필요**:
- [ ] 실제 URL 확인
- [ ] 회의록 페이지 찾기
- [ ] 문서 형식 확인 (PDF/HTML)
- [ ] 페이지 구조 확인

---

### 1.2 City of Holly Springs

**검색 키워드**:
- "Holly Springs Georgia city council meetings"
- "Holly Springs Georgia planning meetings"

**예상 사이트**:
- 공식 웹사이트: https://www.hollyspringsga.us/
- 회의 정보 경로: /government/city-council/meetings/

**조사 필요**:
- [ ] 실제 URL 확인
- [ ] 회의록 페이지 찾기
- [ ] 동적/정적 렌더링 확인
- [ ] 문서 타입 확인

---

### 1.3 City of Alpharetta

**검색 키워드**:
- "Alpharetta Georgia city council meetings"
- "Alpharetta planning commission"

**예상 사이트**:
- 공식 웹사이트: https://www.alpharetta.ga.us/
- 회의 정보 경로: /government/city-council/meetings/

**조사 필요**:
- [ ] 실제 URL 확인
- [ ] 회의록 페이지 찾기
- [ ] 문서 접근성 확인
- [ ] 페이지 구조 확인

---

### 1.4 City of Marietta

**검색 키워드**:
- "Marietta Georgia city council meetings"
- "Marietta planning zoning meetings"

**예상 사이트**:
- 공식 웹사이트: https://www.mariettaga.gov/
- 회의 정보 경로: /government/city-council/meetings/

**조사 필요**:
- [ ] 실제 URL 확인
- [ ] 회의록 페이지 찾기
- [ ] 복잡도 확인
- [ ] 문서 형식 확인

---

## 📊 Step 2: 웹사이트 구조 분석

각 사이트에 대해 다음 항목 조사:

### 분석 항목 체크리스트

#### 기본 정보
- [ ] 회의록 목록 페이지 URL
- [ ] 렌더링 방식 (정적/동적)
- [ ] 페이지네이션 여부
- [ ] 검색 기능 여부

#### 문서 타입
- [ ] Meeting Minutes 제공 여부
- [ ] Meeting Agendas 제공 여부
- [ ] Agenda Packets 제공 여부
- [ ] Video Recordings 제공 여부

#### 기술적 특징
- [ ] HTML 구조 (테이블/리스트/카드)
- [ ] 날짜 형식
- [ ] PDF 링크 패턴
- [ ] JavaScript 의존성

#### 난이도 평가
- [ ] 🟢 쉬움 / 🟡 중간 / 🔴 어려움
- [ ] MVP 적합도 (⭐ 1-5)

---

## 🔍 Step 2.1: Alpharetta CivicClerk 분석 결과

### 기본 정보
- **URL**: https://alpharettaga.portal.civicclerk.com
- **플랫폼**: CivicClerk (SPA)
- **렌더링**: ⚠️ **JavaScript 필수** (Client-side rendering)

### 중요 발견사항

#### JavaScript 의존성 ⚠️
```
페이지 응답: "You need to enable JavaScript to run this app."
```

**의미**:
- CivicClerk 포털은 완전한 JavaScript 기반 SPA
- 서버 렌더링 HTML 없음
- Playwright (또는 유사 도구) **필수**
- BeautifulSoup 단독으로는 불가능

#### 기술적 영향

**장점**:
- ✅ Playwright 기술 검증 기회
- ✅ 동적 사이트 처리 경험 축적
- ✅ 실제 구현 환경과 동일

**단점**:
- ⚠️ 정적 HTML 파싱보다 느림
- ⚠️ 리소스 사용량 증가 (브라우저 실행)
- ⚠️ 복잡도 증가

#### MVP 적합성 재평가

**기존 평가**: ⭐⭐⭐⭐⭐ (가장 쉬움)
**수정 평가**: ⭐⭐⭐⭐ (여전히 적합, 단 Playwright 필수)

**근거**:
- CivicClerk는 표준화된 플랫폼
- Playwright만 추가하면 깔끔한 구조는 유지
- 다른 지자체도 동적 렌더링 가능성 있음
- Playwright 경험이 Phase 2 확장에 도움

### 생성된 도구

#### 1. `fetch_alpharetta_html.py`

**기능**:
- Playwright로 JavaScript 렌더링된 HTML 가져오기
- 전체 페이지 HTML + 스크린샷 저장
- 자동 CSS Selector 패턴 탐색
- BeautifulSoup 구조 분석

**실행 방법**:
```bash
# 의존성 설치
cd /Users/leetangle/code/Note/assignment/zonagent/research
pip install -r requirements.txt
playwright install chromium

# 스크립트 실행
python fetch_alpharetta_html.py
```

**출력**:
- `html_samples/alpharetta_portal_[timestamp].html`: 전체 HTML
- `html_samples/alpharetta_portal_[timestamp].png`: 스크린샷
- `html_samples/sample_meeting_item_[timestamp].html`: 회의 항목 샘플

#### 2. `requirements.txt`

Phase 0 테스트용 패키지:
- `playwright>=1.40.0`
- `beautifulsoup4>=4.12.0`
- `httpx>=0.25.0`
- `lxml>=4.9.0`

### 다음 작업
- [ ] 로컬에서 스크립트 실행
- [ ] HTML 샘플 저장 및 분석
- [ ] CSS Selector 패턴 추출
- [ ] LLM 테스트 (HTML → Selectors)
- [ ] 나머지 3개 지자체 분석 계속

---

## 🔧 Step 3: 기술 스택 검증

### 3.1 Python 환경

```bash
# Python 버전 확인
python --version
# 예상: Python 3.11.x

# 가상환경 테스트
python -m venv test_env
source test_env/bin/activate
```

**체크리스트**:
- [ ] Python 3.11+ 설치 확인
- [ ] venv 생성 테스트

---

### 3.2 웹 스크래핑 도구

```bash
# 패키지 설치 테스트
pip install playwright beautifulsoup4 httpx

# Playwright 설치
playwright install chromium
```

**체크리스트**:
- [ ] Playwright 설치 성공
- [ ] BeautifulSoup4 설치 성공
- [ ] httpx 설치 성공

---

### 3.3 LLM API 테스트

```bash
# Anthropic 패키지
pip install anthropic python-dotenv
```

**테스트 코드**:
```python
import os
from anthropic import Anthropic

# API Key 확인
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ API Key not found")
else:
    print("✅ API Key found")

# 간단한 테스트
client = Anthropic(api_key=api_key)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say hello"}]
)
print("✅ API Test Success:", response.content[0].text)
```

**체크리스트**:
- [ ] API Key 설정
- [ ] API 호출 성공
- [ ] 비용 확인 (~$0.001)

---

## 📝 Step 4: 조사 결과 문서화

### 비교표 작성

| 지자체 | URL | 난이도 | 문서 타입 | 렌더링 | MVP 적합도 |
|--------|-----|--------|-----------|--------|------------|
| Cherokee County | ? | ? | ?/4 | ? | ? |
| Holly Springs | ? | ? | ?/4 | ? | ? |
| Alpharetta | ? | ? | ?/4 | ? | ? |
| Marietta | ? | ? | ?/4 | ? | ? |

### MVP 지자체 선정 기준

**우선순위**:
1. 정적 HTML (Playwright 불필요)
2. 명확한 구조 (테이블)
3. 4가지 문서 타입 모두 제공
4. 표준 날짜 형식
5. 간단한 페이지네이션

**선정**: [조사 후 결정]

---

## ⚠️ 발견된 이슈

### 기술적 이슈
- [ ] 없음

### 접근성 이슈
- [ ] 없음

### 예상 문제점
- [ ] 없음

---

## 📈 진행 상황

- [x] Phase 0 시작
- [x] 웹사이트 URL 확인 (4/4) ✅
- [x] 구조 분석 - Alpharetta 초기 분석 (1/4) 🔄
- [ ] 구조 분석 - 나머지 3개 지자체 (0/3)
- [ ] 기술 검증 (0/3)
- [ ] MVP 선정

**진행 중**:
- ✅ 4개 지자체 URL 발견 완료 (`websites-found.md`)
- 🔄 Alpharetta CivicClerk 구조 분석 중
- ⚠️ **중요 발견**: Alpharetta는 JavaScript 기반 SPA → Playwright 필수

**생성된 도구**:
- `fetch_alpharetta_html.py`: Playwright 기반 HTML 구조 분석 스크립트
- `requirements.txt`: Phase 0 의존성 패키지 목록

**다음 단계**:
1. 로컬 환경에서 `fetch_alpharetta_html.py` 실행
2. 렌더링된 HTML 구조 확인
3. CSS Selector 패턴 추출
4. 나머지 3개 지자체 분석

**예상 완료**: 2025-12-13

---

**최종 업데이트**: 2025-12-12 (Alpharetta 초기 분석 완료)
**작성자**: Implementation Team
