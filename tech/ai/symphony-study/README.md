---
date: 2026-04-01
tags:
  - tech
  - series
  - symphony
  - openai
  - agent-orchestration
status: learning
type: tech-tool-study
---

# OpenAI Symphony

> **한 줄 정의**: 이슈 트래커(Linear)의 작업을 자동으로 감지하고, 격리된 워크스페이스에서 코딩 에이전트(Codex)를 실행하여 PR까지 자율적으로 완성하는 에이전트 오케스트레이션 서비스

## 개요

Symphony는 OpenAI가 2026년 3월에 오픈소스로 공개한 **자율 코딩 에이전트 오케스트레이터**다. 개발자가 코딩 에이전트를 일일이 감독하는 대신, **작업(이슈) 단위로 관리**할 수 있게 해준다. Linear 보드에서 이슈를 감지하면 이슈별 격리된 워크스페이스를 만들고, Codex를 app-server 모드로 실행하여 구현, 테스트, PR 생성, CI 검증까지 자동으로 수행한다.

핵심 철학: **"코딩 에이전트를 감독하지 말고, 작업을 관리하라."**

---

## Quick Start

```bash
# 1. 저장소 클론 및 이동
git clone https://github.com/openai/symphony
cd symphony/elixir

# 2. Elixir 런타임 설치 (mise 사용 권장)
mise trust
mise install

# 3. 의존성 설치 및 빌드
mise exec -- mix setup
mise exec -- mix build

# 4. Linear API 키 설정
export LINEAR_API_KEY="lin_api_xxxxx"

# 5. WORKFLOW.md 커스터마이징 후 실행
mise exec -- ./bin/symphony ./WORKFLOW.md
```

> [!warning] Engineering Preview
> Symphony는 현재 **실험적 엔지니어링 프리뷰** 상태다. 신뢰할 수 있는 환경에서의 테스트 용도로만 권장된다.

---

## 학습 경로

### 1단계: 기초 이해
- [ ] [[01-overview|개요]] 읽기 - 핵심 개념, 아키텍처, 장단점
- [ ] [[02-ecosystem|생태계]] 파악 - LangGraph, CrewAI 등과 비교

### 2단계: 참고자료 확인
- [ ] [[03-references|참고자료]] 확인 - 공식 문서, SPEC.md, 커뮤니티 자료

### 3단계: 핵심 기능 학습
- [ ] [[04-learning/01-architecture|아키텍처]] - 6개 핵심 컴포넌트 이해
- [ ] [[04-learning/02-workflow-config|WORKFLOW.md 설정]] - 워크플로우 정의와 프롬프트 템플릿
- [ ] [[04-learning/03-orchestrator|오케스트레이터]] - 폴링, 스케줄링, 재조정 루프
- [ ] [[04-learning/04-codex-integration|Codex 연동]] - App Server 프로토콜과 세션 관리
- [ ] [[04-learning/05-workspace-management|워크스페이스 관리]] - 격리, 훅, 안전성 보장

### 4단계: 실전 적용
- [ ] [[05-projects|실전 프로젝트]] - 나만의 WORKFLOW.md 작성, 커스텀 구현
- [ ] [[cheatsheet|치트시트]] - 빠른 참조

---

## 파일 구조

```
symphony-study/
├── README.md                          ← 여기 (개요 + 학습 로드맵)
├── 01-overview.md                     ← 핵심 개념, 아키텍처, 장단점, 사용 사례
├── 02-ecosystem.md                    ← 관련 기술 비교 (LangGraph, CrewAI 등)
├── 03-references.md                   ← 공식 문서, SPEC.md, 학습 자료
├── 04-learning/                       ← 실습 가이드
│   ├── 01-architecture.md             ← 6대 컴포넌트 아키텍처
│   ├── 02-workflow-config.md          ← WORKFLOW.md 설정 완전 가이드
│   ├── 03-orchestrator.md             ← 오케스트레이터 상태 머신
│   ├── 04-codex-integration.md        ← Codex App Server 프로토콜
│   └── 05-workspace-management.md     ← 워크스페이스 격리와 훅
├── 05-projects.md                     ← 실전 프로젝트, Best Practices
└── cheatsheet.md                      ← 빠른 참조 (설정 키, 명령어)
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | 핵심 개념, 아키텍처, 장단점, 사용 사례 |
| 생태계 | [[02-ecosystem]] | LangGraph, CrewAI, AutoGen 비교 |
| 참고자료 | [[03-references]] | 공식 SPEC.md, Harness Engineering 문서 |
| 아키텍처 | [[04-learning/01-architecture]] | 6개 컴포넌트 상세 분석 |
| 워크플로우 | [[04-learning/02-workflow-config]] | WORKFLOW.md 작성 가이드 |
| 오케스트레이터 | [[04-learning/03-orchestrator]] | 폴링/스케줄링/재조정 상태 머신 |
| Codex 연동 | [[04-learning/04-codex-integration]] | App Server JSON-RPC 프로토콜 |
| 워크스페이스 | [[04-learning/05-workspace-management]] | 격리, 훅, 안전성 |
| 프로젝트 | [[05-projects]] | 실전 적용 가이드 |
| 치트시트 | [[cheatsheet]] | 빠른 참조 카드 |

---

## 관련 노트

- [[agent-orchestration|에이전트 오케스트레이션 학습 노트]]
- [[langchain-crewai|LangChain-CrewAI]]
- [[ai-ecosystem|AI Ecosystem]]

---

**생성일**: 2026-04-01
**상태**: 학습 중
