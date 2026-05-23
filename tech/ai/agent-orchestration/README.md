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

## 핵심 도구 종합 비교 (2026-03-29 기준)

### Tier 1: 기존 학습 완료

| 비교 항목 | [[conductor/README\|Conductor]] | [[cmux/README\|cmux]] | [[oh-my-claudecode/README\|OMC]] | [[claude-squad/README\|Claude Squad]] | [[vibe-kanban/README\|Vibe Kanban]] |
|-----------|-----------|------|-----|-------------|-------------|
| **유형** | macOS GUI 앱 | 네이티브 터미널 | Claude Code 확장 | CLI (tmux) | CLI + Web UI |
| **격리 방식** | git worktree | 없음 (패널) | 없음 | git worktree | git worktree |
| **지원 에이전트** | CC + Codex | 모든 CLI 에이전트 | Claude Code 전용 | CC/Codex/Aider | CC/Gemini/Amp |
| **Claude 고유기능** | ✅ 100% | ✅ 100% | ✅ (확장 레이어) | ✅ 100% | ✅ 100% |
| **모델 라우팅** | ✗ | ✗ | ✓ (Haiku→Opus) | ✗ | ✗ |
| **가격** | 현재 무료 | 무료 (OSS) | 무료 (OSS) | 무료 (OSS) | 무료 (OSS) |
| **병렬 실행** | ✓ | ✓ (패널) | ✓ (5 workers) | ✓ | ✓ |
| **시각화** | GUI 대시보드 | 터미널 탭 | 터미널 | 터미널 | 칸반 보드 |
| **설치** | DMG 다운로드 | DMG 다운로드 | npm install | brew install | npm install |
| **핵심 차별점** | Checkpoint + GitHub 연동 | 범용 터미널 | 토큰 최적화 30-50% | 심플 + 안정 | 내장 diff 리뷰 |

### Tier 2: 주목할 신규 도구

| 비교 항목 | [[ccmanager/README\|ccmanager]] | [[agent-deck/README\|Agent Deck]] | [[emdash/README\|Emdash]] | [[superset/README\|Superset]] |
|-----------|-----------|------------|--------|----------|
| **유형** | TUI (PTY 기반) | TUI (tmux) | GUI (Electron) | GUI (Electron) |
| **격리 방식** | git worktree | tmux 세션 | git worktree | git worktree |
| **지원 에이전트** | 8종 (CC/Codex/Gemini 등) | CC/Codex/Gemini 등 | **23종** | 모든 CLI 에이전트 |
| **Claude 고유기능** | ✅ 100% | ✅ 100% (Skills Manager) | ✅ 100% (Skills sync) | ✅ 100% |
| **가격** | 무료 (MIT) | 무료 (MIT) | 무료 (MIT) | 무료 (ELv2) |
| **플랫폼** | macOS/Linux | macOS/Linux/Win(WSL) | 전체 | macOS (Win/Linux 예정) |
| **GitHub Stars** | ~970 | ~1,780 | ~3,200 | ~8,120 |
| **핵심 차별점** | tmux 없이 8+ 에이전트 | **실시간 비용 추적** | **Best-of-N 비교** | IDE 연동 (VS Code/JetBrains) |
| **설치** | npm install -g | brew install | brew install --cask | DMG 다운로드 |

### 선택 가이드

| 상황 | 추천 도구 | 이유 |
|------|----------|------|
| GUI 선호 + Claude/Codex | **Conductor** | Checkpoint, GitHub 연동, .context 공유 |
| GUI + 23종 에이전트 | **Emdash** | Best-of-N 비교, 티켓 연동 (YC W26) |
| GUI + IDE 연동 | **Superset** | VS Code/JetBrains 원클릭, 8k+ stars |
| 터미널 + 다양한 에이전트 | **ccmanager** | 8종 에이전트, tmux 불필요, 설치 간편 |
| 터미널 + 비용 추적 | **Agent Deck** | 실시간 비용 대시보드, MCP 관리, 대화 포크 |
| 가벼운 CLI 관리 | **Claude Squad** | brew install 한 줄, tmux 기반 |
| 다양한 CLI 모니터링 | **cmux** | 범용 터미널, 알림 배지, 소켓 API |
| Claude 토큰 비용 절감 | **OMC** | 모델 라우팅으로 30-50% 절감 |
| 팀/프로젝트 관리 | **Vibe Kanban** | 칸반 보드 + PR 스타일 diff 리뷰 |

---

## CLI 코딩 에이전트 비교

> 상세 비교: [[cli-agents|CLI 코딩 에이전트 종합 비교]]

오케스트레이션 도구가 관리하는 대상인 CLI 에이전트들의 비교 (무료 여부 중심):

### 완전 무료 (OSS + BYOK)

| 에이전트 | Stars | 지원 모델 | 언어 | 핵심 차별점 |
|----------|-------|----------|------|------------|
| **Gemini CLI** | ~99K | Gemini 2.5 Pro/Flash | TS | **일 1,000회 무료**, 1M 컨텍스트 |
| **Cline CLI** | ~59.6K | 모든 프로바이더 | TS | Human-in-the-loop, Checkpoint |
| **Aider** | ~42.5K | 100+ 모델 | Python | 가장 성숙, 자동 git 커밋 |
| **Goose** | ~33.7K | 모든 LLM | Rust | Block 12K 직원 실사용, MCP 네이티브 |
| **Pi** | ~28.7K | 15+ 프로바이더 | TS | 미니멀, 4가지 모드 |
| **Qwen Code** | ~21.2K | Qwen3-Coder 480B+ | TS | SWE-bench 69.6%, Gemini CLI 포크 |
| **Hermes** | ~15.4K | 200+ (OpenRouter) | Python | Self-learning, 크론 스케줄러 |
| **OpenCode** | ~11.6K | 75+ 프로바이더 | Go | LSP 자동 설정, 멀티 세션 |

### 유료 (구독/API)

| 에이전트 | Stars | 최저 가격 | 무료 티어 | 핵심 차별점 |
|----------|-------|----------|----------|------------|
| **Claude Code** | ~84K | Pro $20/월 | ❌ | Skills, Hooks, MCP, 서브에이전트 |
| **Codex CLI** | ~68K | Plus $20/월 | 제한적 | Terminal-Bench #1, Rust |
| **Copilot CLI** | ~9.6K | Pro $10/월 | ✅ 제한 | GitHub 네이티브 연동 |
| **Mistral Vibe** | ~3.7K | $14.99/월 | ❌ | 7x 비용 효율, 유럽 |
| **Amp** | N/A | 광고 기반 무료 | ✅ ~$10/일 | Deep mode, 서브에이전트 |
| **Kiro** | ~3.3K | Pro $20/월 | ✅ 50 크레딧 | Spec-driven, Agent Hooks |

---

## 추가 도구 (참고)

### 자율 오케스트레이션

| 도구 | 핵심 | 링크 |
|------|------|------|
| **Composio Agent Orchestrator** | CI 실패 자동 수정, 리뷰 코멘트 자동 대응, SSE 대시보드 | [GitHub](https://github.com/ComposioHQ/agent-orchestrator) |
| **Automaker** | 칸반에 기능 설명 → 에이전트가 자율 구현/테스트/버그수정 | [GitHub](https://github.com/AutoMaker-Org/automaker) |

### 터미널 기반

| 도구 | 핵심 | 링크 |
|------|------|------|
| **dmux** | 11 에이전트 CLI, AI 커밋 메시지, lifecycle hooks (MIT) | [GitHub](https://github.com/standardagents/dmux) |
| **AMUX** | self-healing 무인 실행, 웹 대시보드, 단일 Python 파일 | [GitHub](https://github.com/mixpeek/amux) |
| **Chloe** | 칸반 + 터미널 결합, 100% Rust, 제로 텔레메트리 | [getchloe.sh](https://getchloe.sh) |

### GUI / 데스크톱

| 도구 | 핵심 | 링크 |
|------|------|------|
| **Shannon** | 시각적 DAG 편집기로 에이전트 의존관계 정의 (MIT) | [GitHub](https://github.com/yessGlory17/shannon) |
| **Canopy** | 소스코드 미접근 보안, 자동 상태 추적, CopyTree 기반 | [canopyide.com](https://canopyide.com) |

### 벤더 네이티브

| 도구 | 핵심 | 비고 |
|------|------|------|
| **Claude Code Agent Teams** | Anthropic 공식, 2-16명 팀원 스폰, 에이전트 간 직접 소통 | Opus 4.6부터 |
| **GitHub Agent HQ** | Issue/PR에서 여러 에이전트에 작업 배분 | Copilot 구독 |
| **Google Antigravity** | 5+ 에이전트 동시, 멀티 모델, 무료 프리뷰 | 공개 프리뷰 |
| **Cursor Background Agents** | 클라우드 VM에서 최대 20개 병렬 | Cursor 구독 |

### 기타

| 도구 | 핵심 | 링크 |
|------|------|------|
| **Gas Town** (Steve Yegge) | "AI 에이전트의 Kubernetes" — 20-30개 동시 실행 | [GitHub](https://github.com/steveyegge/gastown) |
| **Sculptor** (Imbue) | Docker 컨테이너 격리, 페어링 모드 | [GitHub](https://github.com/imbue-ai/sculptor) |
| **Conductor-MCP** (GGPrompts) | Claude Code용 MCP 서버, 33개 tmux 도구 | [GitHub](https://github.com/GGPrompts/conductor-mcp) |
| **AgentPipe** | 에이전트 간 대화/토론 "방", 비용 추적 | [agentpipe.ai](https://agentpipe.ai) |

### 큐레이션 리스트

- [awesome-cli-coding-agents](https://github.com/bradAGI/awesome-cli-coding-agents) — 80+ 에이전트 + harness 목록
- [awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators)

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

### 3단계: Tier 2 도구 개요
- [ ] [[ccmanager/01-overview|ccmanager]] — 8종 에이전트, tmux 불필요
- [ ] [[agent-deck/01-overview|Agent Deck]] — 실시간 비용 추적, MCP 관리
- [ ] [[emdash/01-overview|Emdash]] — 23종 에이전트, Best-of-N 비교
- [ ] [[superset/01-overview|Superset]] — IDE 연동, 8k+ stars

### 4단계: 실습
- [ ] 현재 사용 중인 Conductor와 1-2개 대안 도구 직접 비교 테스트
- [ ] 자신의 워크플로우에 최적인 도구 선정

---

## 바로가기

### Tier 1 (상세 학습)

| 도구 | 개요 | 생태계 | 참고자료 |
|------|------|--------|---------|
| Conductor | [[conductor/01-overview]] | [[conductor/02-ecosystem]] | [[conductor/03-references]] |
| cmux | [[cmux/01-overview]] | [[cmux/02-ecosystem]] | [[cmux/03-references]] |
| OMC | [[oh-my-claudecode/01-overview]] | [[oh-my-claudecode/02-ecosystem]] | [[oh-my-claudecode/03-references]] |
| Claude Squad | [[claude-squad/01-overview]] | [[claude-squad/02-ecosystem]] | [[claude-squad/03-references]] |
| Vibe Kanban | [[vibe-kanban/01-overview]] | [[vibe-kanban/02-ecosystem]] | [[vibe-kanban/03-references]] |

### Tier 2 (개요)

| 도구 | 개요 |
|------|------|
| ccmanager | [[ccmanager/01-overview]] |
| Agent Deck | [[agent-deck/01-overview]] |
| Emdash | [[emdash/01-overview]] |
| Superset | [[superset/01-overview]] |

### CLI 코딩 에이전트

| 문서 | 설명 |
|------|------|
| [[cli-agents]] | 18종 CLI 코딩 에이전트 종합 비교 (무료 여부, 벤치마크, 비용 최적화) |

---

## 관련 노트

- [[study/tech/ai/claude/09-agent-teams|Claude Code Agent Teams]]
- [[study/tech/ai/claude/03-claude-code|Claude Code CLI]]
- [[study/tech/ai/ai-ecosystem/01-overview|AI 생태계 개요]]

---

**생성일**: 2026-03-28
**상태**: 학습 중
