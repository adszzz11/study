# ZonAgent 프로젝트 진행 상황

> **최종 업데이트**: 2025-12-15
> **현재 Phase**: Phase 0 완료, Phase A 시작 대기

---

## ✅ 완료된 작업

### Phase 0: 요구사항 분석 및 사전 조사 (완료)

1. **원본 과제 분석**
   - Assignment Description 분석 완료
   - 핵심 요구사항 식별

2. **4개 지자체 플랫폼 사전 조사**
   - Cherokee County (Granicus) - 서버 렌더링
   - City of Marietta (CivicEngage) - 하이브리드
   - City of Alpharetta (CivicClerk) - JavaScript SPA
   - City of Holly Springs (CivicClerk) - JavaScript SPA
   - 상세 분석: `요구사항-분석/research/platform-analysis.md` (~13,000 라인)

3. **요구사항 명세 작성**
   - 클라이언트와 Q&A 진행 (28개 질문)
   - 전체 시스템 아키텍처 설계
   - Python Agent CLI + Spring Boot Kotlin 구조 확정
   - 3단계 데이터 파이프라인 설계
   - Agentic Self-Healing 시스템 설계
   - **문서**: `요구사항-명세.md` (v2.0, ~1,130 라인)

4. **GitHub 레포지토리 설정**
   - Organization: `sm-assign-zonagent`
   - Repository: `sm-zonagent-assignment` (Private)
   - 초기 코드 푸시 완료 (38 files, 16,886 lines)

---

## 📋 현재 상태

### 결정된 사항

#### 1. 아키텍처
```
Spring Boot (Kotlin)
     ↑ POST /api/*       │ subprocess execution
     │                   ↓
Python Agent (CLI)
     ↓
Claude API (LLM)
Playwright
```

**주요 설계 원칙**:
- Python Agent는 DB 직접 접근 ❌
- 모든 데이터는 Kotlin API를 통해 저장/조회
- API는 모두 POST 방식, RequestBody 사용
- Dynamic Trigger System (MANUAL, PERIODIC, CRON, EVENT)

#### 2. 기술 스택

**Backend (Spring Boot - Kotlin)**:
- Spring Boot 3.x
- Kotlin
- PostgreSQL (관계형 데이터)
- MongoDB (문서 메타데이터)
- File System (PDF, 추출 규칙 JSON)

**Scraper (Python Agent - CLI)**:
- Python 3.11+
- Claude API (Anthropic)
- Playwright (JavaScript 렌더링)
- httpx (HTTP 요청)

#### 3. 데이터 파이프라인 (3단계)

**Stage 1: Scraping & Storage**
```
LLM 규칙 생성 → 데이터 추출 → 신뢰성 검증
                              ↓
                        confidence < 0.8?
                              ↓ Yes
                        규칙 재생성 → 재실행
```

**Stage 2: Data Cleaning**
- Minutes PDF → .md 변환 (LLM)
- 기타 PDF → 다운로드 + 링크

**Stage 3: Key Data Extraction**
- 회의 정보, 안건, 결정사항, 요약 추출 (LLM)

#### 4. 구현 범위

**지자체** (4개 전부):
- Cherokee County
- City of Marietta
- City of Alpharetta
- City of Holly Springs

**문서 타입** (4개 전부):
- Agendas
- Minutes
- Videos (링크만)
- Supporting Documents

**운영 모드**:
- Backfill Mode: 과거 데이터 수집
- Continuous Mode: 주기적 업데이트

---

## 🎯 다음 단계: Phase A 시작

### Phase A 목표
**Cherokee County 전체 파이프라인 구현 (MVP)**

예상 기간: 2-3주

### Phase A 작업 항목

#### 1. 프로젝트 초기 설정

**Python Agent 프로젝트**:
```bash
mkdir python-agent
cd python-agent
python3 -m venv venv
source venv/bin/activate
pip install anthropic playwright httpx pydantic
playwright install
```

**디렉토리 구조**:
```
python-agent/
├── agent/
│   ├── __init__.py
│   ├── main.py              # CLI 진입점
│   ├── orchestrator.py      # 전체 프로세스 조율
│   ├── rule_generator.py    # LLM 규칙 생성
│   ├── data_extractor.py    # 데이터 추출
│   ├── validator.py         # 신뢰성 검증
│   └── api_client.py        # Kotlin API 호출
├── scrapers/
│   ├── __init__.py
│   ├── base.py              # 베이스 스크래퍼
│   └── cherokee.py          # Cherokee County 스크래퍼
├── models/
│   ├── __init__.py
│   └── dto.py               # 데이터 모델 (Pydantic)
├── config.py
├── requirements.txt
└── README.md
```

**Spring Boot Kotlin 프로젝트**:
```bash
# Spring Initializr 또는 IDE로 생성
# Dependencies: Web, JPA, PostgreSQL, MongoDB, Validation
```

**디렉토리 구조**:
```
kotlin-backend/
├── src/main/kotlin/com/zonagent/
│   ├── ZonagentApplication.kt
│   ├── controller/
│   │   ├── ScraperController.kt    # POST /api/scraper/*
│   │   ├── MeetingController.kt    # POST /api/meetings/*
│   │   └── FileController.kt       # POST /api/files/*
│   ├── service/
│   │   ├── ScraperService.kt
│   │   ├── MeetingService.kt
│   │   ├── SchedulerService.kt     # Dynamic Trigger
│   │   └── ProcessExecutor.kt      # Python subprocess
│   ├── domain/
│   │   ├── Meeting.kt
│   │   ├── Document.kt
│   │   └── ScraperConfig.kt
│   ├── repository/
│   │   ├── MeetingRepository.kt    # PostgreSQL
│   │   └── DocumentRepository.kt   # MongoDB
│   └── dto/
│       ├── request/
│       └── response/
└── src/main/resources/
    └── application.yml
```

#### 2. 환경 변수 설정

**`.env` 파일 생성 (Python)**:
```bash
CLAUDE_API_KEY=sk-ant-api03-...
KOTLIN_API_BASE_URL=http://localhost:8080
```

**`application.yml` (Kotlin)**:
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/zonagent
    username: postgres
    password: [설정 필요]
  data:
    mongodb:
      uri: mongodb://localhost:27017/zonagent

python:
  agent:
    path: ${PYTHON_AGENT_PATH:../python-agent}
    venv: ${PYTHON_VENV_PATH:../python-agent/venv}
```

#### 3. API 엔드포인트 구현 우선순위

**Phase A-1: Scraper Control API (Kotlin)**
```kotlin
POST /api/scraper/trigger
  {
    "jurisdictionId": "cherokee",
    "mode": "BACKFILL",
    "dateRange": { "from": "2024-01-01", "to": "2024-12-31" }
  }

POST /api/scraper/config/get
  { "jurisdictionId": "cherokee" }

POST /api/scraper/config/update
  {
    "jurisdictionId": "cherokee",
    "triggerType": "PERIODIC",
    "intervalMinutes": 1440
  }
```

**Phase A-2: Data Reception API (Kotlin)**
```kotlin
POST /api/meetings/bulk
  {
    "jurisdictionId": "cherokee",
    "meetings": [...]
  }

POST /api/files/upload
  {
    "meetingId": "...",
    "fileType": "MINUTES_PDF",
    "file": <multipart>
  }
```

**Phase A-3: Python Agent 구현**
- CLI 진입점 (`python -m agent --jurisdiction cherokee --mode backfill`)
- Kotlin API 호출 (httpx)
- Cherokee County 스크래퍼 (서버 렌더링이므로 Playwright 불필요)
- 규칙 생성 (Claude API)
- 데이터 추출
- 신뢰성 검증

#### 4. Cherokee County 스크래핑 구현

**URL**: https://cherokeega.granicus.com/ViewPublisher.php?view_id=2

**문서 타입별 구현**:
1. Agendas 추출
2. Minutes 추출
3. Videos 링크 추출
4. Supporting Documents 추출

**Stage 1 구현**:
- LLM에게 HTML 제공 → 추출 규칙 생성
- 규칙 기반 데이터 추출
- 신뢰성 검증 (confidence score)
- 재시도 로직 (confidence < 0.8)

#### 5. Stage 2, 3 구현

**Stage 2: Data Cleaning**
- Minutes PDF → .md 변환 (Claude API)
- PDF 다운로드 및 저장

**Stage 3: Key Data Extraction**
- 회의 정보 추출
- 안건 추출
- 결정사항 추출
- 요약 생성

#### 6. 테스트 및 검증

- Cherokee County 2024년 전체 데이터 수집
- 데이터 정확성 검증
- Confidence score 분석
- 재시도 횟수 분석

---

## 📂 주요 문서 참조

### 필수 읽기

1. **요구사항-명세.md** (⭐ 최우선)
   - 전체 시스템 아키텍처
   - API 명세
   - 데이터베이스 스키마
   - Agentic 시스템 설계
   - Phase별 로드맵

2. **요구사항-분석/research/platform-analysis.md**
   - Cherokee County HTML 구조 분석
   - CSS Selector 정보
   - 렌더링 방식

3. **요구사항-분석/Assignment-Description.md**
   - 원본 과제 요구사항

### 참고 자료

- **README.md**: 프로젝트 개요
- **요구사항-분석/research/websites-found.md**: 4개 지자체 URL

---

## 🔑 환경 설정 체크리스트

### 필수 설치 항목

- [ ] Python 3.11+
- [ ] Java 17+
- [ ] PostgreSQL 14+
- [ ] MongoDB 6+
- [ ] Node.js (Playwright 실행용)

### API 키 발급

- [ ] Claude API 키 (https://console.anthropic.com/)
  - 모델: `claude-3-5-sonnet-20241022` 사용 예정
  - Rate limit 확인 필요

### 데이터베이스 설정

- [ ] PostgreSQL 데이터베이스 생성: `zonagent`
- [ ] MongoDB 데이터베이스 생성: `zonagent`
- [ ] 파일 저장 경로 설정: `./data/files/`

---

## 🚀 시작 가이드

### 1. 레포지토리 클론
```bash
git clone https://github.com/sm-assign-zonagent/sm-zonagent-assignment.git
cd sm-zonagent-assignment
```

### 2. 문서 읽기
```bash
# 필수: 요구사항 명세 확인
cat 요구사항-명세.md

# Cherokee County 플랫폼 분석 확인
cat 요구사항-분석/research/platform-analysis.md | grep -A 100 "Cherokee County"
```

### 3. 프로젝트 생성
```bash
# Python Agent 프로젝트 생성
mkdir python-agent
cd python-agent
python3 -m venv venv
source venv/bin/activate

# Spring Boot Kotlin 프로젝트 생성 (IDE 사용 권장)
# 또는 Spring Initializr: https://start.spring.io/
```

### 4. Phase A 시작
- `DEVELOPMENT-GUIDE.md` 참조 (다음 커밋에 추가 예정)
- API 명세는 `요구사항-명세.md` 3.2절 참조
- DB 스키마는 `요구사항-명세.md` 3.5절 참조

---

## 📊 Phase별 예상 일정

| Phase | 목표 | 예상 기간 | 상태 |
|-------|------|-----------|------|
| **Phase 0** | 요구사항 분석 및 사전 조사 | 1주 | ✅ 완료 |
| **Phase A** | Cherokee County 전체 파이프라인 | 2-3주 | ⏳ 대기 |
| **Phase B** | 3개 지자체 추가 (총 4개) | 1-2주 | 📅 예정 |
| **Phase C** | Continuous 모드 + 비디오 링크 | 1주 | 📅 예정 |
| **Phase D** | 프로덕션 준비 (문서화, 테스트) | 2주 | 📅 예정 |
| **총계** | | **6-8주** | |

---

## 💡 중요 노트

### Agentic 시스템 핵심
- **규칙 생성**: LLM이 HTML 구조를 보고 추출 규칙 자동 생성
- **Self-Healing**: 신뢰성이 낮으면 자동으로 규칙 재생성
- **검증**: 추출된 데이터를 LLM이 필드별로 검증

### 확장 가능성
- 새로운 지자체 추가 시 코드 수정 최소화
- 규칙 기반이므로 HTML 변경에 자동 적응
- Playwright로 JavaScript SPA 지원

### 프로덕션 고려사항
- Rate Limiting (Claude API)
- Error Handling & Retry
- Logging & Monitoring
- Data Validation
- Security (API 키 관리)

---

**작성자**: Claude Code
**마지막 업데이트**: 2025-12-15
**다음 작업자**: Phase A 시작 - Python Agent 프로젝트 초기 설정부터 시작
