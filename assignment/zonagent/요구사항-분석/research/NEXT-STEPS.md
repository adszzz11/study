# 다음 단계: Alpharetta HTML 구조 분석

> Phase 0.2: 로컬 환경에서 실행해야 할 작업들

## 🎯 현재 상황

✅ **완료된 작업**:
- 4개 지자체 웹사이트 URL 발견
- Alpharetta CivicClerk 포털이 JavaScript SPA임을 확인
- HTML 구조 분석 스크립트 생성 (`fetch_alpharetta_html.py`)

⏳ **다음 작업**:
- 로컬에서 스크립트 실행하여 실제 HTML 획득
- CSS Selector 패턴 추출
- LLM 테스트

---

## 📋 로컬 실행 체크리스트

### Step 1: 환경 설정 (최초 1회)

```bash
# 1. 연구 디렉터리로 이동
cd /Users/leetangle/code/Note/assignment/zonagent/research

# 2. 가상환경 생성 (권장)
python3 -m venv venv
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. Playwright 브라우저 설치 (~100MB)
playwright install chromium
```

**예상 시간**: 3-5분
**디스크 용량**: ~200MB (Chromium 브라우저)

---

### Step 2: Alpharetta HTML 구조 분석

```bash
# 스크립트 실행
python fetch_alpharetta_html.py
```

**예상 출력**:
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
    1. Agenda                 -> /meetings/agenda/123
    2. Minutes                -> /meetings/minutes/123
    ...

✅ 분석 완료!
```

**예상 시간**: 10-15초
**생성 파일**:
- `html_samples/alpharetta_portal_*.html` (전체 HTML)
- `html_samples/alpharetta_portal_*.png` (스크린샷)
- `html_samples/sample_meeting_item_*.html` (회의 항목 샘플)

---

### Step 3: 결과 확인

```bash
# 1. 생성된 파일 확인
ls -lh html_samples/

# 2. 스크린샷 보기 (macOS)
open html_samples/alpharetta_portal_*.png

# 3. HTML 샘플 보기 (처음 50줄)
head -n 50 html_samples/sample_meeting_item_*.html

# 또는 전체 HTML 파일을 브라우저로 열기
open html_samples/alpharetta_portal_*.html
```

---

## 🔍 분석할 내용

HTML 샘플을 확인하면서 다음 정보를 찾아야 합니다:

### 1. 회의 목록 구조

**찾을 내용**:
- 회의 항목들이 어떻게 나열되어 있는가?
  - `<table>` 형식?
  - `<ul>` 리스트?
  - `<div>` 카드?
- CSS 클래스명은 무엇인가?
- 각 회의 항목의 HTML 구조는?

**예시 패턴**:
```html
<!-- 예상 구조 1: 테이블 -->
<table class="meeting-list">
  <tr class="meeting-row" data-meeting-id="123">
    <td class="date">12/05/2024</td>
    <td class="title">Planning Commission Meeting</td>
    <td class="documents">
      <a href="/agenda/123.pdf">Agenda</a>
      <a href="/minutes/123.pdf">Minutes</a>
    </td>
  </tr>
</table>

<!-- 예상 구조 2: 리스트 -->
<ul class="meetings">
  <li class="meeting-item">
    <span class="date">12/05/2024</span>
    <h3 class="title">Planning Commission Meeting</h3>
    <div class="docs">...</div>
  </li>
</ul>
```

### 2. 날짜 형식

**찾을 내용**:
- 날짜가 어떤 형식으로 표시되는가?
  - `MM/DD/YYYY`? (예: 12/05/2024)
  - `YYYY-MM-DD`? (예: 2024-12-05)
  - 텍스트? (예: December 5, 2024)

### 3. 문서 링크 패턴

**찾을 내용**:
- Agenda, Minutes, Packets, Videos 링크가 어떻게 구분되는가?
- 링크 URL 패턴은?
  - `/meetings/agenda/123`?
  - `/documents/123/agenda.pdf`?
- 문서 타입을 어떻게 알 수 있는가?
  - 링크 텍스트? (예: "Agenda", "Minutes")
  - CSS 클래스? (예: `class="doc-agenda"`)
  - URL 패턴? (예: `href="/agenda/..."`)

### 4. 페이지네이션

**찾을 내용**:
- 회의 목록에 페이지네이션이 있는가?
- "다음 페이지" 버튼은 어떻게 구현되어 있는가?
- 전체 회의 개수를 알 수 있는가?

---

## 📝 CSS Selector 추출

HTML 구조를 파악한 후, 다음 CSS Selector들을 추출해야 합니다:

```python
# 예시 Selector 목록 (실제 HTML 보고 결정)
SELECTORS = {
    "meeting_rows": "table.meeting-list tr.meeting-row",
    "meeting_date": "td.date",
    "meeting_title": "td.title",
    "agenda_link": "a[href*='agenda']",
    "minutes_link": "a[href*='minutes']",
    "packet_link": "a[href*='packet']",
    "video_link": "a[href*='video']",
    "next_page": "a.pagination-next",
}
```

---

## 🤖 LLM 테스트 (선택사항)

HTML 샘플이 준비되면, LLM이 CSS Selector를 자동으로 생성할 수 있는지 테스트합니다.

### 테스트 스크립트 (생성 예정):

```python
# test_llm_selector.py
from anthropic import Anthropic
import os
from pathlib import Path

# HTML 샘플 읽기
html_file = Path("html_samples").glob("sample_meeting_item_*.html")
html_content = list(html_file)[0].read_text()

# LLM에게 Selector 생성 요청
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
prompt = f"""
다음은 회의 정보를 담은 HTML 코드입니다.
이 HTML에서 다음 정보를 추출하기 위한 CSS Selector를 생성해주세요:

1. 회의 날짜
2. 회의 제목
3. Agenda PDF 링크
4. Minutes PDF 링크

HTML:
{html_content}

JSON 형식으로 반환:
{{"date": "...", "title": "...", "agenda": "...", "minutes": "..."}}
"""

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)
```

**예상 비용**: ~$0.001 per request

---

## ✅ 완료 조건

다음 정보가 모두 확보되면 Step 2 완료:

- [ ] HTML 샘플 저장 완료
- [ ] 회의 목록 구조 파악 (테이블/리스트/카드)
- [ ] CSS Selector 추출 완료
- [ ] 날짜 형식 확인
- [ ] 문서 링크 패턴 확인
- [ ] 페이지네이션 방식 확인
- [ ] (선택) LLM Selector 생성 테스트 완료

---

## 🚀 Step 2 완료 후

다음 작업들:

### 1. 나머지 3개 지자체 분석
- Cherokee County (Granicus)
- Holly Springs (CivicClerk + IQM2)
- Marietta (CivicEngage)

### 2. MVP 지자체 최종 확정
- 4개 지자체 비교 분석
- 최종 MVP 선정 (현재: Alpharetta 유력)

### 3. Phase 1 시작 준비
- 프로젝트 구조 생성
- 데이터 모델 구현
- 첫 스크래퍼 작성

---

## ⚠️ 트러블슈팅

### 문제 1: Playwright 설치 실패

**증상**: `playwright install` 실패

**해결**:
```bash
# 권한 문제
sudo playwright install chromium

# 또는 개별 사용자 설치
playwright install --with-deps chromium
```

### 문제 2: Python 버전 문제

**증상**: `No module named 'dataclasses'`

**해결**:
```bash
# Python 3.11+ 필요
python3 --version

# pyenv 사용 시
pyenv install 3.11.7
pyenv local 3.11.7
```

### 문제 3: 스크립트 실행 중 타임아웃

**증상**: `TimeoutError: Page didn't load in 30s`

**해결**:
- 인터넷 연결 확인
- 스크립트의 `wait_for_timeout` 값 증가
- VPN 사용 시 비활성화

### 문제 4: 빈 HTML 파일 생성

**증상**: HTML 파일이 거의 비어있음

**해결**:
- JavaScript 렌더링 대기 시간 증가 (`await page.wait_for_timeout(5000)`)
- `wait_until="networkidle"` → `wait_until="load"` 변경

---

## 📞 도움 요청

문제가 계속되면:
1. 에러 메시지 전체 복사
2. `python --version` 출력
3. `pip list` 출력
4. 스크린샷 (있다면)

위 정보와 함께 문의하세요.

---

**작성일**: 2025-12-12
**Phase**: 0.2 - Alpharetta HTML 구조 분석
**예상 소요 시간**: 30-60분
