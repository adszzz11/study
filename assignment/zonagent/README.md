# ZonAgent

> Georgia 지자체 공공 문서 자동 수집 시스템 - 요구사항 분석

## 🎯 프로젝트 개요

Georgia주 4개 지자체의 Planning & Zoning 회의 문서를 자동으로 수집하는 스크래퍼 시스템 개발 과제입니다.

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
└── 삭제/                        # 🗑️ 삭제 예정 파일
    ├── 프로젝트-문서/           # 이전 구현 완료 보고서
    ├── 계획/                    # 이전 구현 계획
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

---

## 🎯 현재 상태

- ✅ 요구사항 분석 완료
- ✅ Phase 0 사전 조사 완료 (4개 플랫폼 분석)
- 🔄 계획 재검토 필요

---

**작성일**: 2025-12-10 ~ 2025-12-14
**상태**: 📋 요구사항 분석 완료
