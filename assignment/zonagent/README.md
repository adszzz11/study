# ZonAgent

> Georgia 지자체 공공 문서 자동 수집 시스템 - 계획 및 요구사항 분석

## 🎯 프로젝트 개요

Georgia주 4개 지자체의 Planning & Zoning 회의 문서를 자동으로 수집하는 스크래퍼 시스템 개발 프로젝트입니다.

### 목표

Georgia주 4개 지자체의 공공 회의 문서를 자동으로 수집하여 데이터베이스에 저장:
- Meeting Agendas (회의 안건)
- Meeting Minutes (회의록)
- Agenda Packets (안건 패킷)

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
├── 요구사항-분석/               # 📋 요구사항 및 사전 조사
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
├── 계획/                        # 📝 구현 계획 및 설계
│   ├── README.md
│   ├── IMPLEMENTATION-MASTER.md # 마스터 플랜
│   └── implementation-plan/     # Phase별 상세 계획
│       ├── detailed-design.md
│       ├── phase-0-research.md
│       ├── phase-1-mvp.md
│       ├── phase-2-expansion.md
│       └── phase-3-completion.md
│
└── 삭제/                        # 🗑️ 삭제 예정 파일
    ├── 프로젝트-문서/           # 구현 완료 보고서 (구현 후 작성 예정)
    └── research-불필요파일/     # Phase 0 진행 과정 기록
```

---

## 📚 주요 문서

### 시작하기

1. **[요구사항-분석/Assignment-Description.md](요구사항-분석/Assignment-Description.md)**
   - 원본 과제 설명서

2. **[요구사항-분석/과제-분석.md](요구사항-분석/과제-분석.md)**
   - 과제 핵심 요구사항 분석

### 요구사항 분석

1. **[요구사항-분석/요구사항-분류.md](요구사항-분석/요구사항-분류.md)**
   - 요구사항 상세 분류

2. **[요구사항-분석/분류-요약.md](요구사항-분석/분류-요약.md)**
   - 요구사항 분류 요약

3. **[요구사항-분석/specs/](요구사항-분석/specs/)**
   - 확실한 요구사항 명세
   - 검토 필요 사항

### 사전 조사 결과 (Phase 0)

1. **[요구사항-분석/research/platform-analysis.md](요구사항-분석/research/platform-analysis.md)**
   - 4개 플랫폼 상세 분석
   - HTML 구조 및 CSS Selector
   - 렌더링 방식 비교

2. **[요구사항-분석/research/websites-found.md](요구사항-분석/research/websites-found.md)**
   - URL 발견 과정
   - MVP 지자체 선정 근거

### 구현 계획

1. **[계획/IMPLEMENTATION-MASTER.md](계획/IMPLEMENTATION-MASTER.md)** ⭐
   - 전체 구현 마스터 플랜
   - 무엇을, 어떻게, 왜 만드는가
   - 설계 결정 근거

2. **[계획/implementation-plan/README.md](계획/implementation-plan/README.md)**
   - Phase별 실행 계획 개요
   - 타임라인 및 성공 지표

3. **Phase별 상세 계획**:
   - [phase-0-research.md](계획/implementation-plan/phase-0-research.md) - 사전 조사
   - [phase-1-mvp.md](계획/implementation-plan/phase-1-mvp.md) - MVP 개발
   - [phase-2-expansion.md](계획/implementation-plan/phase-2-expansion.md) - 확장 개발
   - [phase-3-completion.md](계획/implementation-plan/phase-3-completion.md) - 완성 및 제출

---

## 🏗️ 계획된 아키텍처

### 기술 스택

```python
# Core
Python 3.11+
httpx          # HTTP 요청 (서버 렌더링)
BeautifulSoup4 # HTML 파싱
Playwright     # 브라우저 자동화 (JavaScript SPA)
SQLite3        # 데이터베이스
Claude API     # LLM Agentic 시스템

# CLI
argparse       # 명령줄 인터페이스
```

### 핵심 설계

1. **Hybrid Agentic 시스템**
   - LLM으로 CSS Selector 자동 추출
   - Rule Cache로 재사용 (비용 절감)

2. **Plugin Architecture**
   - 지자체별 Scraper 독립 구현
   - 확장 용이

3. **Strategy Pattern**
   - 플랫폼별 렌더링 전략 선택

---

## 📊 예상 개발 계획

| Phase | 작업 내용 | 예상 시간 |
|-------|----------|-----------|
| Phase 0 | 사전 조사 및 분석 | 9h |
| Phase 1 | Cherokee County MVP | 6h |
| Phase 2 | 3개 지자체 추가 | 4h |
| Phase 3 | 문서화 및 완성 | 10h |
| **총계** | | **29h** |

---

## 🎯 현재 상태

- ✅ 요구사항 분석 완료
- ✅ Phase 0 사전 조사 완료
- ✅ 구현 계획 수립 완료
- ⏳ 구현 대기 중

---

## 🔮 다음 단계

Phase 1 MVP 개발 시작:
1. Cherokee County 스크래퍼 구현
2. LLM Agent 통합
3. SQLite 데이터베이스
4. CLI 인터페이스

**참고**: [계획/implementation-plan/phase-1-mvp.md](계획/implementation-plan/phase-1-mvp.md)

---

**작성일**: 2025-12-10 ~ 2025-12-11
**상태**: 📋 계획 완료, 구현 준비 완료
