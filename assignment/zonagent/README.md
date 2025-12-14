# ZonAgent

> Georgia 지자체 공공 문서 자동 수집 시스템 - Agentic Document Scraper

## 🎯 프로젝트 개요

Georgia주 4개 지자체의 Planning & Zoning 회의 문서를 LLM 기반 Agentic 시스템으로 자동 수집하는 프로젝트입니다.

### 핵심 목표

1. **완전한 커버리지**: 4개 지자체 + 4개 문서 타입 전부 구현
2. **Agentic 시스템**: LLM이 규칙 생성 → 데이터 추출 → 검증 → Self-healing
3. **프로덕션 준비**: 실제 배포 가능한 완성된 시스템

### 대상 지자체

| 지자체 | 플랫폼 | 렌더링 방식 | 난이도 |
|--------|--------|-------------|--------|
| Cherokee County | Granicus | 서버 렌더링 | 🟢 쉬움 |
| City of Marietta | CivicEngage | 하이브리드 | 🟢 쉬움 |
| City of Alpharetta | CivicClerk | JavaScript SPA | 🟡 중간 |
| City of Holly Springs | CivicClerk | JavaScript SPA | 🟡 중간 |

---

## 📁 프로젝트 구조

```
zonagent/
├── README.md                    # 👈 이 파일 (프로젝트 소개)
│
├── 요구사항-명세.md              # ⭐ 최종 요구사항 명세서
│
├── 요구사항-분석/               # 📋 요구사항 분석 및 사전 조사
│   ├── README.md
│   ├── Assignment-Description.md # 원본 과제 설명
│   ├── 요구사항-분류.md
│   ├── 과제-분석.md
│   ├── 분류-요약.md
│   ├── research/                # Phase 0 사전 조사 결과
│   │   ├── platform-analysis.md # 4개 플랫폼 상세 분석
│   │   └── websites-found.md    # URL 발견 및 MVP 선정
│   └── specs/                   # 요구사항 스펙
│       ├── 1-확실한-요구사항/
│       └── 2-검토-필요-사항/
│
└── 삭제/                        # 🗑️ 이전 버전 파일
    ├── 프로젝트-문서/           # 이전 구현 완료 보고서
    ├── 계획/                    # 이전 구현 계획
    └── research-불필요파일/     # Phase 0 진행 과정 기록
```

---

## 📚 주요 문서

### ⭐ 필수 읽기

**[요구사항-명세.md](요구사항-명세.md)** - 최종 요구사항 명세서
- 전체 시스템 아키텍처
- 기능 요구사항 상세
- 기술 스택 및 설계
- 데이터 파이프라인
- Agentic 시스템 설계
- Phase별 로드맵

### 원본 과제

**[요구사항-분석/Assignment-Description.md](요구사항-분석/Assignment-Description.md)**
- 원본 과제 설명서

### 사전 조사 결과

**[요구사항-분석/research/platform-analysis.md](요구사항-분석/research/platform-analysis.md)**
- 4개 플랫폼 상세 분석
- HTML 구조 및 CSS Selector
- 렌더링 방식 비교

**[요구사항-분석/research/websites-found.md](요구사항-분석/research/websites-found.md)**
- URL 발견 과정
- MVP 지자체 선정 근거

---

## 🏗️ 시스템 아키텍처 (요약)

### 기술 스택

```
Spring Boot (Kotlin)     ←→  Python FastAPI
     ↓                            ↓
PostgreSQL              Claude API (LLM)
MongoDB                 Playwright
File System
```

### 3단계 데이터 파이프라인

```
1. Scraping & Storage
   → LLM 규칙 생성 → 데이터 추출 → 신뢰성 검증

2. Data Cleaning
   → Minutes PDF → .md 변환
   → 기타 PDF → 다운로드 + 링크

3. Key Data Extraction
   → 회의 정보, 안건, 결정사항, 요약 추출
```

### Agentic Self-Healing

```
규칙 생성 → 데이터 추출 → 신뢰성 검증
                              ↓
                        confidence < 0.8?
                              ↓ Yes
                        규칙 재생성 → 재실행
```

---

## 📊 Phase별 로드맵

| Phase | 목표 | 예상 기간 |
|-------|------|-----------|
| **Phase A** | Cherokee County 전체 파이프라인 | 2-3주 |
| **Phase B** | 3개 지자체 추가 (총 4개) | 1-2주 |
| **Phase C** | Continuous 모드 + 비디오 링크 | 1주 |
| **Phase D** | 프로덕션 준비 (문서화, 테스트, 인프라) | 2주 |
| **총계** | | **6-8주** |

---

## 🎯 현재 상태

- ✅ 원본 과제 분석 완료
- ✅ Phase 0 사전 조사 완료 (4개 플랫폼 분석)
- ✅ **요구사항 명세 완료**
- ⏳ Phase A 구현 시작 대기

---

## 🚀 다음 단계

**Phase A 시작 준비**:
1. 개발 환경 설정
2. Python FastAPI 프로젝트 생성
3. Spring Boot Kotlin 프로젝트 생성
4. Claude API 키 발급
5. Cherokee County 스크래퍼 구현 시작

---

**작성일**: 2025-12-10 ~ 2025-12-14
**상태**: 📋 요구사항 명세 완료, 구현 준비 완료
