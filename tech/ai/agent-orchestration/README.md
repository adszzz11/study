---
date: 2026-03-28
tags:
  - tech
  - ai
  - agent-orchestration
status: learning
type: tech-tool-study
---

# AI 에이전트 오케스트레이션 플랫폼

> **한 줄 정의**: AI 코딩 에이전트(Claude Code, Gemini CLI, Codex 등)를 병렬로 실행하고 관리하는 도구 생태계

## 개요

AI 코딩 에이전트가 단일 세션에서 벗어나 **다중 병렬 실행**으로 진화하면서, 이를 효율적으로 관리하는 오케스트레이션 도구들이 등장했다. 주요 관심사는:

- **병렬 실행**: 여러 에이전트를 동시에 돌려 작업 처리량 극대화
- **격리**: git worktree 등으로 에이전트 간 충돌 방지
- **관리**: 세션 모니터링, 결과 리뷰, 머지 워크플로우

---

## 핵심 도구 종합 비교

| 비교 항목 | [[conductor/README\|Conductor]] | [[cmux/README\|cmux]] | [[oh-my-claudecode/README\|OMC]] | [[claude-squad/README\|Claude Squad]] | [[vibe-kanban/README\|Vibe Kanban]] |
|-----------|-----------|------|-----|-------------|-------------|
| **유형** | macOS 앱 | 네이티브 터미널 | Claude Code 확장 | CLI (tmux) | CLI + Web UI |
| **격리 방식** | git worktree | 없음 (패널) | 없음 | git worktree | git worktree |
| **지원 에이전트** | Claude Code | 모든 CLI 에이전트 | Claude Code 전용 | CC/Codex/Aider | CC/Gemini/Amp |
| **모델 라우팅** | ✗ | ✗ | ✓ (Haiku→Opus) | ✗ | ✗ |
| **가격** | 유료 | 무료 (OSS) | 무료 (OSS) | 무료 (OSS) | 무료 (OSS) |
| **병렬 실행** | ✓ | ✓ (패널) | ✓ (5 workers) | ✓ | ✓ |
| **시각화** | GUI 대시보드 | 터미널 탭 | 터미널 | 터미널 | 칸반 보드 |
| **설치** | DMG 다운로드 | DMG 다운로드 | npm install | brew install | npm install |
| **핵심 차별점** | 시각적 UX | 범용 터미널 | 토큰 최적화 30-50% | 심플 + 안정 | 내장 diff 리뷰 |

### 선택 가이드

| 상황 | 추천 도구 | 이유 |
|------|----------|------|
| GUI 선호 + macOS | Conductor | 시각적 대시보드, 직관적 UX |
| 다양한 CLI 에이전트 사용 | cmux | 에이전트 무관하게 모든 CLI 지원 |
| Claude 토큰 비용 절감 | OMC | 모델 라우팅으로 30-50% 절감 |
| 가벼운 CLI 관리 | Claude Squad | brew install 한 줄, tmux 기반 |
| 팀/프로젝트 관리 필요 | Vibe Kanban | 칸반 보드 + PR 스타일 diff 리뷰 |

---

## CLI 에이전트 간략 비교

오케스트레이션 도구가 관리하는 대상인 CLI 에이전트들의 비교:

| 에이전트 | 제공사 | 기본 모델 | 가격 | 특징 |
|----------|--------|----------|------|------|
| **Claude Code** | Anthropic | Claude Opus/Sonnet | Max $100-200/월 | MCP, Skills, Hooks, 서브에이전트 |
| **Gemini CLI** | Google | Gemini 2.5 Pro | 무료 (일 1000회) | 1M 토큰 컨텍스트, Google Search |
| **Codex** | OpenAI | GPT-4o/o3 | Plus $20/월~ | Rust 기반, 서브에이전트 |
| **Aider** | 오픈소스 | 다중 모델 | 무료 (API 비용) | 50+ 언어, 자동 git 커밋 |
| **Amp** | Sourcegraph | 다중 모델 | 일일 무료 크레딧 | 무제한 토큰, 세션 공유 |

---

## 추가 도구 (참고)

### Composio Agent Orchestrator
- 에이전트 플릿 관리, CI 수정/머지 충돌 자동 처리
- 에이전트/런타임/트래커 무관 (Claude Code, Codex, Aider + tmux, Docker + GitHub, Linear)
- [GitHub](https://github.com/ComposioHQ/agent-orchestrator)

### Gas Town (Steve Yegge)
- "AI 에이전트의 Kubernetes" — 20-30개 에이전트 동시 실행
- 역할 기반 아키텍처 (Mayor, Polecats, Witness 등)
- 실험 단계, 시간당 ~$100 비용
- [GitHub](https://github.com/steveyegge/gastown)

### Sculptor (Imbue)
- Docker 컨테이너 격리로 에이전트 실행
- 페어링 모드로 컨테이너 작업을 로컬 repo로 가져오기
- 베타 단계, Claude Code/Codex 지원
- [GitHub](https://github.com/imbue-ai/sculptor)

### Conductor-MCP (GGPrompts)
- Claude Code용 MCP 서버, 33개 tmux 관리 도구
- TTS 통합, 실시간 모니터링
- [GitHub](https://github.com/GGPrompts/conductor-mcp)

---

## 트렌드 (2026)

1. **단일 코파일럿 → 분산 에이전트 시스템**: 한 명의 AI 어시스턴트에서 역할별 전문 에이전트 팀으로 진화
2. **격리가 핵심 인프라**: git worktree / Docker 컨테이너로 에이전트 간 충돌 방지
3. **모델 라우팅 최적화**: 작업 복잡도에 따라 경량/중량 모델 자동 선택
4. **시장 규모**: 2026년 $8.5B → 2030년 $35B 예상

---

## 학습 경로

### 1단계: 개요 파악
- [ ] 이 README의 비교표 이해
- [ ] 각 도구의 [[conductor/01-overview|개요]] 읽기

### 2단계: 깊이 있는 비교
- [ ] [[conductor/02-ecosystem|Conductor 생태계]]
- [ ] [[cmux/02-ecosystem|cmux 생태계]]
- [ ] [[oh-my-claudecode/02-ecosystem|OMC 생태계]]
- [ ] [[claude-squad/02-ecosystem|Claude Squad 생태계]]
- [ ] [[vibe-kanban/02-ecosystem|Vibe Kanban 생태계]]

### 3단계: 실습
- [ ] 현재 사용 중인 Conductor와 1-2개 대안 도구 직접 비교 테스트
- [ ] 자신의 워크플로우에 최적인 도구 선정

---

## 바로가기

| 도구 | 개요 | 생태계 | 참고자료 |
|------|------|--------|---------|
| Conductor | [[conductor/01-overview]] | [[conductor/02-ecosystem]] | [[conductor/03-references]] |
| cmux | [[cmux/01-overview]] | [[cmux/02-ecosystem]] | [[cmux/03-references]] |
| OMC | [[oh-my-claudecode/01-overview]] | [[oh-my-claudecode/02-ecosystem]] | [[oh-my-claudecode/03-references]] |
| Claude Squad | [[claude-squad/01-overview]] | [[claude-squad/02-ecosystem]] | [[claude-squad/03-references]] |
| Vibe Kanban | [[vibe-kanban/01-overview]] | [[vibe-kanban/02-ecosystem]] | [[vibe-kanban/03-references]] |

---

## 관련 노트

- [[study/tech/ai/claude/09-agent-teams|Claude Code Agent Teams]]
- [[study/tech/ai/claude/03-claude-code|Claude Code CLI]]
- [[study/tech/ai/ai-ecosystem/01-overview|AI 생태계 개요]]

---

**생성일**: 2026-03-28
**상태**: 학습 중
