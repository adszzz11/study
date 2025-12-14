# Phase 0: 사전 조사 및 분석

> 실제 구현 전에 모든 지자체 웹사이트를 조사하고 기술적 실현 가능성 검증

## 🎯 Phase 목표

**주요 목표:**
1. ✅ 4개 지자체 웹사이트 구조 완전 파악
2. ✅ 기술 스택 실현 가능성 검증
3. ✅ MVP 개발에 가장 적합한 지자체 선정
4. ✅ 프로젝트 기본 구조 및 개발 환경 설정

**예상 기간**: 1-2일 (8-16시간)

**성공 기준:**
- 각 지자체별 상세 분석 리포트 작성
- Playwright로 모든 사이트 접근 성공
- LLM API 테스트 성공
- MVP 지자체 확정 및 근거 문서화

---

## 📋 Step-by-Step 실행 계획

### Step 1: 개발 환경 설정 (1-2시간)

#### 1.1 Python 환경 구축

**액션:**
```bash
# 1. Python 버전 확인 (3.11 이상 권장)
python --version

# 2. 가상환경 생성
python -m venv venv

# 3. 가상환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 4. uv 설치 (빠른 패키지 관리)
pip install uv

# 5. 기본 패키지 설치
uv pip install playwright beautifulsoup4 httpx anthropic python-dotenv
```

**체크리스트:**
- [ ] Python 3.11+ 설치 확인
- [ ] 가상환경 생성 및 활성화
- [ ] uv 설치
- [ ] 기본 패키지 설치 완료

---

#### 1.2 Playwright 설정

**액션:**
```bash
# Playwright 브라우저 설치
playwright install chromium

# 테스트 스크립트 실행
python -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

**체크리스트:**
- [ ] Chromium 브라우저 설치
- [ ] Playwright import 테스트 성공

---

#### 1.3 API Key 설정

**액션:**
```bash
# .env 파일 생성
cat > .env << EOF
ANTHROPIC_API_KEY=your_api_key_here
# OPENAI_API_KEY=your_api_key_here  # Optional
EOF

# .gitignore에 추가
echo ".env" >> .gitignore
```

**테스트 스크립트:**
```python
# test_api.py
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello!"}]
)

print("API Test Success:", response.content[0].text)
```

**체크리스트:**
- [ ] Anthropic API Key 발급
- [ ] .env 파일 생성
- [ ] API 테스트 성공
- [ ] .gitignore 설정

---

### Step 2: 프로젝트 구조 생성 (30분)

**액션:**
```bash
# 프로젝트 디렉터리 구조 생성
mkdir -p zonagent-scraper/{scraper/{core,jurisdictions,utils,config},data/{documents,rules},tests,docs}

cd zonagent-scraper

# 기본 파일 생성
touch scraper/__init__.py
touch scraper/core/{__init__.py,base_scraper.py,llm_agent.py,storage.py}
touch scraper/jurisdictions/__init__.py
touch scraper/utils/__init__.py
touch scraper/config/__init__.py
touch README.md
touch pyproject.toml
```

**디렉터리 구조:**
```
zonagent-scraper/
├── scraper/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base_scraper.py      # 추상 베이스 클래스
│   │   ├── llm_agent.py          # LLM 통합
│   │   └── storage.py            # 저장 로직
│   ├── jurisdictions/
│   │   └── __init__.py           # 지자체별 플러그인
│   ├── utils/
│   │   └── __init__.py           # 유틸리티
│   └── config/
│       └── __init__.py           # 설정
├── data/
│   ├── documents/                # 다운로드한 문서
│   └── rules/                    # LLM 생성 규칙
├── tests/
│   └── __init__.py
├── docs/
│   └── research/                 # 조사 결과
├── .env
├── .gitignore
├── README.md
└── pyproject.toml
```

**체크리스트:**
- [ ] 디렉터리 구조 생성
- [ ] 기본 __init__.py 파일 생성
- [ ] README.md 생성

---

### Step 3: 지자체 웹사이트 조사 (3-6시간)

각 지자체별로 동일한 조사 프로세스 진행

#### 3.1 Cherokee County (비법인 지역)

**조사 항목:**

**1. 웹사이트 찾기**
```bash
# Google 검색
"Cherokee County Georgia planning zoning meetings"
"Cherokee County meeting minutes agendas"
```

**2. 사이트 구조 분석**
- [ ] **URL 확인**: 회의 문서가 있는 메인 페이지
- [ ] **문서 목록 형식**: 테이블? 리스트? 카드?
- [ ] **렌더링 방식**: 정적 HTML? JavaScript?
- [ ] **페이지네이션**: 있는가? 형식은?
- [ ] **날짜 형식**: 어떤 포맷인가?
- [ ] **문서 타입 구분**: Minutes/Agenda/Packet 구분 방법

**3. 기술적 분석**
```python
# research/test_cherokee.py
from playwright.sync_api import sync_playwright

def analyze_cherokee():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 브라우저 보이게
        page = browser.new_page()

        # 회의 페이지 방문
        url = "http://..."  # 실제 URL
        page.goto(url)

        # 페이지 로드 대기
        page.wait_for_load_state("networkidle")

        # HTML 구조 확인
        html = page.content()

        # 스크린샷 저장
        page.screenshot(path="docs/research/cherokee_screenshot.png")

        # HTML 저장
        with open("docs/research/cherokee_sample.html", "w") as f:
            f.write(html)

        browser.close()

        print(f"✅ Cherokee County analyzed")
        print(f"📸 Screenshot: docs/research/cherokee_screenshot.png")
        print(f"📄 HTML: docs/research/cherokee_sample.html")

if __name__ == "__main__":
    analyze_cherokee()
```

**4. 문서 작성**
```markdown
# docs/research/cherokee-county-analysis.md

## Cherokee County

### 기본 정보
- **URL**: [실제 URL]
- **조사 날짜**: 2025-12-11
- **상태**: ✅ 조사 완료

### 사이트 구조
- **문서 위치**: [경로]
- **목록 형식**: 테이블/리스트/기타
- **렌더링**: 정적/동적(React/Vue 등)
- **페이지네이션**: 있음/없음

### 문서 타입
- **Minutes**: [발견 여부, 형식, 링크 패턴]
- **Agendas**: [발견 여부, 형식, 링크 패턴]
- **Packets**: [발견 여부, 형식, 링크 패턴]
- **Videos**: [발견 여부, 호스팅 플랫폼]

### 기술적 특징
- **CSS Selectors**: [주요 선택자]
- **날짜 형식**: MM/DD/YYYY, YYYY-MM-DD 등
- **PDF 링크 패턴**: [패턴]
- **특이사항**: [JavaScript 필요 여부, 인증 등]

### 난이도 평가
- **스크래핑 난이도**: 🟢 쉬움 / 🟡 중간 / 🔴 어려움
- **이유**: [구체적 설명]

### MVP 적합성
- **적합도**: ⭐⭐⭐⭐⭐ (5점 만점)
- **이유**: [선정 근거]

### 예상 문서 수 (1년)
- **예상 회의 수**: ~24개 (월 2회 가정)
- **예상 문서 수**: ~70-100개
```

**체크리스트:**
- [ ] 웹사이트 URL 확인
- [ ] 스크린샷 저장
- [ ] HTML 샘플 저장
- [ ] 분석 문서 작성

---

#### 3.2 City of Holly Springs

**동일한 프로세스 반복**

**체크리스트:**
- [ ] 웹사이트 URL 확인
- [ ] 스크린샷 저장
- [ ] HTML 샘플 저장
- [ ] 분석 문서 작성

---

#### 3.3 City of Alpharetta

**동일한 프로세스 반복**

**체크리스트:**
- [ ] 웹사이트 URL 확인
- [ ] 스크린샷 저장
- [ ] HTML 샘플 저장
- [ ] 분석 문서 작성

---

#### 3.4 City of Marietta

**동일한 프로세스 반복**

**체크리스트:**
- [ ] 웹사이트 URL 확인
- [ ] 스크린샷 저장
- [ ] HTML 샘플 저장
- [ ] 분석 문서 작성

---

### Step 4: 비교 분석 및 MVP 지자체 선정 (1-2시간)

#### 4.1 지자체별 비교표 작성

**문서**: `docs/research/comparison.md`

```markdown
# 지자체 비교 분석

| 지자체 | 난이도 | 문서 타입 | 렌더링 | 날짜 형식 | MVP 적합도 | 비고 |
|--------|--------|-----------|--------|-----------|------------|------|
| Cherokee County | 🟢 쉬움 | 4/4 | 정적 | MM/DD/YYYY | ⭐⭐⭐⭐⭐ | 명확한 구조 |
| Holly Springs | 🟡 중간 | 3/4 | 동적 | YYYY-MM-DD | ⭐⭐⭐ | React 사용 |
| Alpharetta | 🟢 쉬움 | 4/4 | 정적 | MM/DD/YYYY | ⭐⭐⭐⭐ | 잘 정리됨 |
| Marietta | 🔴 어려움 | 2/4 | 동적 | Custom | ⭐⭐ | 복잡한 구조 |

## MVP 선정

**선정**: Cherokee County

**이유**:
1. 정적 HTML (Playwright 불필요, BeautifulSoup만 사용)
2. 명확한 CSS 구조
3. 4가지 문서 타입 모두 제공
4. 표준 날짜 형식
5. 페이지네이션 간단

## 2차 선정 (확장 시)

1순위: Alpharetta (유사 구조)
2순위: Holly Springs (동적이지만 패턴 명확)
3순위: Marietta (가장 복잡, 마지막에 도전)
```

**체크리스트:**
- [ ] 비교표 작성
- [ ] MVP 지자체 선정 및 근거 문서화
- [ ] 확장 순서 결정

---

#### 4.2 공통 패턴 식별

**문서**: `docs/research/common-patterns.md`

```markdown
# 공통 패턴 식별

## 공통 요소

### 1. 문서 목록 표시
- **3개 지자체**: HTML 테이블 사용
- **1개 지자체**: div + 리스트

**공통 추상화 가능**: ✅ 예

### 2. 날짜 형식
- **2개**: MM/DD/YYYY
- **1개**: YYYY-MM-DD
- **1개**: Custom

**공통 추상화 가능**: ✅ 날짜 파싱 유틸 필요

### 3. PDF 링크
- **모두**: 직접 링크 또는 중간 페이지

**공통 추상화 가능**: ✅ 두 패턴 모두 지원

## BaseScaper 인터페이스 제안

```python
class BaseScraper(ABC):
    @abstractmethod
    def get_meeting_list_url(self) -> str:
        """회의 목록 페이지 URL"""
        pass

    @abstractmethod
    def parse_meeting_list(self, html: str) -> List[Meeting]:
        """회의 목록 파싱"""
        pass

    @abstractmethod
    def get_document_links(self, meeting: Meeting) -> List[Document]:
        """회의별 문서 링크 추출"""
        pass
```
```

**체크리스트:**
- [ ] 공통 패턴 문서화
- [ ] BaseScraper 인터페이스 설계
- [ ] 재사용 가능한 유틸리티 식별

---

### Step 5: 기술 스택 검증 (2-3시간)

#### 5.1 Playwright 테스트

**목적**: 동적 페이지 렌더링 검증

**테스트 스크립트**:
```python
# tests/verify_playwright.py
from playwright.sync_api import sync_playwright
import time

def test_dynamic_site():
    """동적 사이트 테스트 (Holly Springs 예시)"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 동적 사이트 방문
        page.goto("http://...")

        # JavaScript 실행 대기
        page.wait_for_load_state("networkidle")

        # 특정 요소 대기
        page.wait_for_selector("table.meetings", timeout=10000)

        # 내용 확인
        content = page.content()
        assert "meeting" in content.lower()

        browser.close()
        print("✅ Playwright 동적 렌더링 테스트 성공")

if __name__ == "__main__":
    test_dynamic_site()
```

**체크리스트:**
- [ ] 정적 사이트 테스트 성공
- [ ] 동적 사이트 테스트 성공
- [ ] 페이지 로드 시간 측정

---

#### 5.2 BeautifulSoup 테스트

**목적**: HTML 파싱 검증

**테스트 스크립트**:
```python
# tests/verify_beautifulsoup.py
from bs4 import BeautifulSoup
import httpx

def test_html_parsing():
    """정적 HTML 파싱 테스트"""
    # Cherokee County 예시
    response = httpx.get("http://...")
    soup = BeautifulSoup(response.text, 'html.parser')

    # 테이블 찾기
    table = soup.find('table', class_='meetings')
    assert table is not None

    # 행 추출
    rows = table.find_all('tr')
    assert len(rows) > 0

    print(f"✅ BeautifulSoup 테스트 성공: {len(rows)}개 행 발견")

if __name__ == "__main__":
    test_html_parsing()
```

**체크리스트:**
- [ ] HTML 파싱 테스트 성공
- [ ] CSS Selector 검증
- [ ] 날짜/링크 추출 테스트

---

#### 5.3 LLM 통합 테스트

**목적**: Claude API로 HTML 분석 가능성 검증

**테스트 스크립트**:
```python
# tests/verify_llm.py
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def test_llm_html_analysis():
    """LLM으로 HTML 구조 분석 테스트"""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # 샘플 HTML 로드
    with open("docs/research/cherokee_sample.html", "r") as f:
        html = f.read()

    # 프롬프트
    prompt = f"""
Analyze this HTML page and extract CSS selectors for meeting documents.

Goal: Find all links to meeting minutes.

HTML (truncated to first 5000 chars):
{html[:5000]}

Return JSON with:
- document_links_selector: CSS selector for document links
- date_selector: CSS selector for dates
- title_selector: CSS selector for titles
- confidence: 0-1 score
"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.content[0].text
    print("✅ LLM 분석 결과:")
    print(result)

    # 비용 확인
    print(f"\n💰 토큰 사용량:")
    print(f"  Input: {response.usage.input_tokens}")
    print(f"  Output: {response.usage.output_tokens}")

    # 대략적 비용 (Claude 3.5 Sonnet 기준)
    cost = (response.usage.input_tokens * 0.003 / 1000 +
            response.usage.output_tokens * 0.015 / 1000)
    print(f"  예상 비용: ${cost:.4f}")

if __name__ == "__main__":
    test_llm_html_analysis()
```

**체크리스트:**
- [ ] LLM API 호출 성공
- [ ] HTML 분석 응답 확인
- [ ] 비용 측정 ($0.01-0.05 예상)
- [ ] JSON 파싱 가능 여부 확인

---

### Step 6: Phase 0 산출물 정리 (1시간)

#### 6.1 문서 정리

**체크리스트:**
- [ ] `docs/research/` 폴더 정리
  - [ ] 4개 지자체 분석 문서
  - [ ] 스크린샷 및 HTML 샘플
  - [ ] 비교 분석 문서
  - [ ] 공통 패턴 문서

---

#### 6.2 기술 검증 리포트 작성

**문서**: `docs/research/tech-validation-report.md`

```markdown
# 기술 검증 리포트

## 검증 항목

| 기술 | 상태 | 비고 |
|------|------|------|
| Playwright | ✅ 성공 | 동적 사이트 지원 확인 |
| BeautifulSoup | ✅ 성공 | 정적 파싱 문제없음 |
| Claude API | ✅ 성공 | HTML 분석 가능, 비용 $0.02/호출 |
| httpx | ✅ 성공 | HTTP 요청 문제없음 |

## 예상 비용

### LLM 비용 (Hybrid 방식)
- 초기 학습: 4개 지자체 x $2 = $8
- Backfill: ~300개 문서 x $0.01 = $3
- **Phase 1 예상**: ~$11

## 기술 스택 확정

✅ **최종 선택**:
- Python 3.11+
- Playwright (동적 사이트용)
- BeautifulSoup4 (정적 파싱용)
- httpx (HTTP 클라이언트)
- Claude 3.5 Sonnet (LLM)
- SQLite (메타데이터)
```

**체크리스트:**
- [ ] 기술 검증 리포트 작성
- [ ] 예상 비용 산정
- [ ] 최종 기술 스택 확정

---

#### 6.3 Phase 1 준비사항 정리

**문서**: `docs/phase-1-prep.md`

```markdown
# Phase 1 준비사항

## MVP 지자체
**선정**: Cherokee County

## 첫 번째 문서 타입
**선정**: Meeting Minutes

## 기본 구조
- ✅ 프로젝트 구조 생성 완료
- ✅ 개발 환경 설정 완료
- ✅ API Key 설정 완료

## 다음 단계
1. BaseScraper 추상 클래스 구현
2. CherokeeScraper 구현
3. LLM Agent 통합
4. 로컬 저장 로직

## 예상 일정
- Day 1: 스크래퍼 기본 구조
- Day 2: LLM 통합
- Day 3: 저장 로직 + 테스트
```

**체크리스트:**
- [ ] MVP 지자체 확정 문서화
- [ ] Phase 1 준비사항 정리
- [ ] 다음 단계 액션 아이템 정리

---

## 📊 Phase 0 완료 체크리스트

### 개발 환경
- [ ] Python 3.11+ 설치
- [ ] 가상환경 생성 및 활성화
- [ ] 필수 패키지 설치
- [ ] Playwright 브라우저 설치
- [ ] API Key 설정 및 테스트

### 프로젝트 구조
- [ ] 디렉터리 구조 생성
- [ ] 기본 파일 생성
- [ ] .gitignore 설정

### 지자체 조사
- [ ] Cherokee County 분석 완료
- [ ] Holly Springs 분석 완료
- [ ] Alpharetta 분석 완료
- [ ] Marietta 분석 완료
- [ ] 비교 분석 완료

### 기술 검증
- [ ] Playwright 테스트 성공
- [ ] BeautifulSoup 테스트 성공
- [ ] LLM API 테스트 성공
- [ ] 비용 측정 완료

### 문서화
- [ ] 4개 지자체 분석 문서
- [ ] 비교 분석 문서
- [ ] 공통 패턴 문서
- [ ] 기술 검증 리포트
- [ ] Phase 1 준비사항

---

## ⚠️ 주의사항 및 팁

### 웹사이트 조사 시
- **예의 바르게**: 너무 빠른 요청은 피하기
- **스크린샷**: 나중에 참고하기 위해 반드시 저장
- **HTML 샘플**: 오프라인 테스트용으로 저장
- **robots.txt 확인**: 차단된 경로 확인

### LLM 테스트 시
- **HTML 크기**: 큰 HTML은 잘라서 전송 (5000-10000자)
- **비용 주의**: 테스트는 1-2회만
- **응답 저장**: 나중에 참고하기 위해 저장

### 시간 관리
- **조사에 집중**: 구현하고 싶어도 참기
- **완벽 추구 금지**: 80%면 충분
- **문서화 우선**: 나중에 까먹지 않도록

---

## 🎯 성공 기준

### 최소 성공
- ✅ 4개 지자체 웹사이트 URL 확인
- ✅ MVP 지자체 선정
- ✅ 개발 환경 설정 완료
- ✅ 기본 프로젝트 구조 생성

### 이상적 성공
- ✅ 4개 지자체 상세 분석 완료
- ✅ 공통 패턴 식별 및 문서화
- ✅ 기술 스택 검증 완료
- ✅ 예상 비용 산정 완료
- ✅ Phase 1 구체적 계획 수립

---

## 📝 산출물 (Deliverables)

1. **분석 문서** (4개)
   - `docs/research/cherokee-county-analysis.md`
   - `docs/research/holly-springs-analysis.md`
   - `docs/research/alpharetta-analysis.md`
   - `docs/research/marietta-analysis.md`

2. **비교 문서**
   - `docs/research/comparison.md`
   - `docs/research/common-patterns.md`

3. **기술 검증**
   - `docs/research/tech-validation-report.md`
   - `tests/verify_playwright.py`
   - `tests/verify_beautifulsoup.py`
   - `tests/verify_llm.py`

4. **샘플 데이터**
   - 스크린샷 (4개)
   - HTML 샘플 (4개)

5. **프로젝트 구조**
   - 완성된 디렉터리 구조
   - 설정 파일 (.env, .gitignore)

---

**다음 단계**: [Phase 1: MVP 개발](./phase-1-mvp.md)

**작성일**: 2025-12-11
**예상 완료**: Phase 0 시작 후 1-2일
