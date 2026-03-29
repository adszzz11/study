---
date: 2026-03-29
tags:
  - tech
  - agent-deck
  - overview
parent: "[[README]]"
---

# Agent Deck - 개요

> [[README|목차로 돌아가기]]

---

## 1. What - Agent Deck란?

> **한 줄 정의**: 실시간 비용 추적 + MCP 관리 + 대화 포크가 가능한 AI 에이전트 TUI 세션 매니저

### 핵심 개념

Agent Deck은 Claude Code, Codex, Gemini CLI 등을 tmux 세션에서 관리하면서, **실시간 토큰 비용 추적**과 **예산 제한**, **MCP 서버 관리**, **대화 포크(context 상속)** 등 고급 기능을 제공하는 Go 기반 TUI 도구다. Claude Code의 transcript 파일을 읽어 비용을 자동 수집하며, Skills/Hooks/CLAUDE.md 등 고유기능이 100% 보존된다.

### 지원 에이전트

| 에이전트 | 통합 레벨 |
|----------|----------|
| **Claude Code** | Full (상태 감지, MCP 관리, 세션 포크, resume, Skills Manager) |
| **Gemini CLI** | Full (상태 감지, MCP, resume, hook 기반 세션 동기화) |
| **Codex** | 상태 감지, conductor 지원 |
| **Cursor** (터미널 모드) | 상태 감지 |
| **OpenCode** | 상태 감지 |
| 커스텀 도구 | `config.toml`의 `[tools.*]`로 설정 |

### Claude Code 고유기능 보존

- **OAuth**: ✅ (config_dir 관리, `CLAUDE_CONFIG_DIR` 환경변수 지원)
- **CLAUDE.md**: ✅ (worktree의 cwd에서 자동 읽기)
- **Skills**: ✅ (**Skills Manager** — 프로젝트별 스킬 attach/detach)
- **Hooks**: ✅ (transcript 파일 읽기로 비용 추적에도 활용)
- **MCP 서버**: ✅ (TUI에서 config 파일 수정 없이 관리)
- **Plugin**: `/plugin marketplace add asheshgoplani/agent-deck`로 Claude Code 플러그인 설치 가능

### 동작 방식

```
Agent Deck (TUI / Go)
├── Claude Code 세션 (tmux)  [busy] — $12.50 today
│   └── Skills: /study, /commit 연결
├── Codex 세션 (tmux)        [idle] — $3.20 today
├── Gemini CLI 세션 (tmux)   [waiting] — $0 (무료 티어)
│
├── [$ 키] 비용 대시보드 — 일/주/월별, 모델별, 세션별
├── [f 키] 대화 포크 — context 상속하여 분기
└── [G 키] 전체 대화 검색
```

---

## 2. 핵심 특징

### 킬러 피처: 실시간 비용 추적

- Claude Code hook 연동으로 transcript에서 자동 수집
- 9개 모델 가격 지원 (Opus/Sonnet/Haiku, Gemini Pro/Flash, GPT-4o/4.1, o3, o4-mini)
- **일일 가격 자동 갱신**
- TUI 대시보드 (`$` 키) + Web 대시보드 (`/costs` 페이지, Chart.js)
- 예산 한도: 일/주/월/그룹/세션별 설정 가능 (80% 경고, 100% 차단)
- CSV/JSON 내보내기

### 기타 장점

- **대화 포크**: `f` 키로 현재 대화를 복제하면서 context 상속
- **MCP 관리**: config 파일 수정 없이 TUI에서 attach/detach
- **Skills Manager**: 프로젝트별 Claude Code 스킬 풀 관리
- **AI 상태 감지**: thinking 중인지 / input 대기 중인지 자동 구분
- **원격 SSH 세션**: 원격 서버의 에이전트도 관리
- **Vimium 스타일 점프 모드**: 빠른 세션 전환
- **무료 (MIT)**: 활발한 개발

### 단점

- **git worktree 격리 없음**: tmux 세션 기반 (Conductor/Claude Squad 대비)
- **tmux 의존**: tmux 필수
- **Gemini/Codex 비용 추적**: output 파싱 방식 (untested 표기)

---

## 3. 설치

```bash
# curl
curl -fsSL https://raw.githubusercontent.com/asheshgoplani/agent-deck/main/install.sh | bash

# Homebrew
brew install asheshgoplani/tap/agent-deck

# Go
go install github.com/asheshgoplani/agent-deck/cmd/agent-deck@latest

# 자동 업데이트
# config.toml에서 auto_update = true
```

설정: `config.toml` (전역) 또는 프로젝트별

---

## 4. 개발 현황

| 항목 | 값 |
|------|-----|
| 버전 | v0.27.5 (2026-03-27) |
| Stars | ~1,780 |
| 라이선스 | MIT |
| 언어 | Go 1.24+ (Bubble Tea TUI) |
| 생성일 | 2025-12-03 |
| 릴리스 속도 | 2-3일마다 |

---

## References

- [GitHub](https://github.com/asheshgoplani/agent-deck)
- [Discord](https://discord.gg/e4xSs6NBN8)
