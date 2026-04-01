---
date: 2026-04-01
tags:
  - tech
  - symphony
  - openai
  - references
parent: "[[README]]"
---

# Symphony - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-architecture|다음: 아키텍처]]

---

## 1. 공식 자료

### GitHub 저장소

- [openai/symphony](https://github.com/openai/symphony) - 메인 저장소
  - `SPEC.md` - 언어 무관 서비스 사양서 (가장 중요한 문서)
  - `elixir/` - 레퍼런스 Elixir 구현
  - `elixir/WORKFLOW.md` - 예제 워크플로우 설정
  - `elixir/AGENTS.md` - Codex를 위한 프로젝트 가이드라인
  - `.codex/skills/` - commit, push, pull, land, linear, debug 스킬

### OpenAI 공식 문서

| 자료 | URL | 설명 |
|------|-----|------|
| Harness Engineering | [openai.com/index/harness-engineering](https://openai.com/index/harness-engineering/) | Symphony의 기반 방법론 |
| Codex App Server | [developers.openai.com/codex/app-server](https://developers.openai.com/codex/app-server/) | App Server JSON-RPC 프로토콜 |
| Codex Subagents | [developers.openai.com/codex/subagents](https://developers.openai.com/codex/subagents) | Codex 서브에이전트 가이드 |
| Codex Harness 아키텍처 | [openai.com/index/unlocking-the-codex-harness](https://openai.com/index/unlocking-the-codex-harness/) | App Server 구축 배경 |

---

## 2. SPEC.md 핵심 구조

SPEC.md는 Symphony의 **정수**다. 13개 섹션으로 구성:

| 섹션 | 내용 | 핵심 포인트 |
|------|------|------------|
| 1. Problem Statement | 문제 정의 | 4가지 운영 문제 해결 |
| 2. Goals / Non-Goals | 목표/비목표 | DB 없는 복구, 범용 워크플로우 엔진 아님 |
| 3. System Overview | 시스템 구성도 | 8개 컴포넌트, 6개 추상화 레이어 |
| 4. Core Domain Model | 도메인 모델 | Issue, Workspace, RunAttempt, LiveSession 등 |
| 5. Workflow Spec | WORKFLOW.md 사양 | 프론트매터 + 프롬프트 템플릿 |
| 6. Configuration | 설정 사양 | 동적 리로드, 디스패치 검증 |
| 7. Orchestration SM | 상태 머신 | Unclaimed -> Claimed -> Running -> Released |
| 8. Polling/Scheduling | 폴링/스케줄링 | 후보 선택, 동시성 제어, 재시도 |
| 9. Workspace Mgmt | 워크스페이스 관리 | 안전성 불변식 3개 |
| 10. Agent Runner | 에이전트 실행 | Codex App Server JSON-RPC 프로토콜 |
| 11. Observability | 옵저버빌리티 | 구조화 로그, 상태 서페이스 |
| 12. Error Handling | 에러 처리 | 5개 에러 클래스 |
| 13. Extension Points | 확장점 | SSH 워커, 서버, 동적 툴 |

---

## 3. 핵심 파일 가이드

### 반드시 읽어야 할 파일 (우선순위순)

```
1. SPEC.md                    → 전체 설계 이해 (필수)
2. elixir/README.md           → Quick Start + 설정 가이드
3. elixir/WORKFLOW.md         → 워크플로우 실제 예시
4. elixir/AGENTS.md           → 구현 코드베이스 규칙
5. elixir/lib/symphony_elixir/
   ├── orchestrator.ex        → 핵심 상태 머신 구현
   ├── agent_runner.ex        → 에이전트 실행 로직
   ├── codex/app_server.ex    → Codex JSON-RPC 클라이언트
   ├── workspace.ex           → 워크스페이스 생명주기
   ├── config.ex              → 설정 파싱/검증
   ├── workflow.ex            → WORKFLOW.md 파싱
   └── tracker.ex             → Linear API 어댑터
```

### 스킬(Skills) 파일

```
.codex/skills/
├── commit/SKILL.md    → 깔끔한 커밋 생성 규칙
├── push/SKILL.md      → 리모트 브랜치 푸시 규칙
├── pull/SKILL.md      → origin/main 동기화 규칙
├── land/              → PR 머지 (land) 프로세스
│   ├── SKILL.md
│   └── land_watch.py  → CI 모니터링 스크립트
├── linear/SKILL.md    → Linear 이슈 조작 규칙
└── debug/SKILL.md     → 디버깅 가이드
```

---

## 4. 커뮤니티 자료

### 기술 블로그 / 분석

| 자료 | URL | 특징 |
|------|-----|------|
| MarkTechPost 분석 | [marktechpost.com](https://www.marktechpost.com/2026/03/05/openai-releases-symphony-an-open-source-agentic-framework-for-orchestrating-autonomous-ai-agents-through-structured-scalable-implementation-runs/) | 출시 분석 |
| Digital Applied 가이드 | [digitalapplied.com](https://www.digitalapplied.com/blog/openai-symphony-autonomous-code-orchestration-framework) | 기술 구조 분석 |
| Medium - AI Engineering | [medium.com](https://ai-engineering-trend.medium.com/openai-releases-symphony-the-agile-kanban-for-the-ai-era-ea72f783adc2) | Agile Kanban 관점 비교 |
| DeepWiki 분석 | [deepwiki.com/openai/symphony](https://deepwiki.com/openai/symphony) | 코드 구조 상세 분석 |
| SJ Ramblings | [sjramblings.io](https://sjramblings.io/openai-symphony-autonomous-agent-orchestration/) | Sprint Board 연동 관점 |
| Ry Walker Research | [rywalker.com](https://rywalker.com/research/symphony) | 연구자 관점 분석 |

### 프레임워크 비교 자료

| 자료 | URL | 비교 대상 |
|------|-----|----------|
| Agent Harness 비교 | [agent-harness.ai](https://agent-harness.ai/blog/agentic-ai-frameworks-2026-langgraph-vs-crewai-vs-autogen-vs-openai-symphony/) | LangGraph, CrewAI, AutoGen, Symphony |
| Turing 비교 | [turing.com](https://www.turing.com/resources/ai-agent-frameworks) | Top 6 프레임워크 |
| Particula 비교 | [particula.tech](https://particula.tech/blog/langgraph-vs-crewai-vs-openai-agents-sdk-2026) | LangGraph, CrewAI, OpenAI Agents SDK |

---

## 5. 관련 기술 문서

| 기술 | 학습 자료 | 용도 |
|------|----------|------|
| Elixir | [elixir-lang.org](https://elixir-lang.org/) | Symphony 레퍼런스 구현 언어 |
| OTP (GenServer) | [Elixir GenServer 가이드](https://hexdocs.pm/elixir/GenServer.html) | Orchestrator 구현 패턴 |
| Phoenix LiveView | [phoenixframework.org](https://www.phoenixframework.org/) | 옵저버빌리티 대시보드 |
| Linear API | [developers.linear.app](https://developers.linear.app/docs) | 이슈 트래커 API |
| JSON-RPC 2.0 | [jsonrpc.org/specification](https://www.jsonrpc.org/specification) | Codex App Server 프로토콜 기반 |
| mise | [mise.jdx.dev](https://mise.jdx.dev/) | Elixir/Erlang 버전 관리 |

---

## 6. 학습 로드맵 제안

### 입문자 (1-2시간)

1. README.md 읽기
2. SPEC.md의 1-3번 섹션 (Problem, Goals, Overview) 읽기
3. elixir/README.md로 Quick Start 시도

### 중급자 (반나절)

1. SPEC.md 전체 정독
2. elixir/WORKFLOW.md 분석
3. orchestrator.ex, agent_runner.ex 코드 리딩
4. 자신의 저장소에 WORKFLOW.md 작성 시도

### 고급자 (1-2일)

1. SPEC.md 기반 다른 언어(Python/Go)로 자체 구현
2. Linear + Codex 연동 실제 실행
3. 커스텀 스킬 작성
4. SSH 원격 워커 설정

---

## 다음 단계

> [!tip] 다음으로
> [[04-learning/01-architecture|아키텍처 학습]]에서 Symphony의 6개 핵심 컴포넌트를 상세히 분석합니다.
