---
date: 2026-03-29
tags:
  - tech
  - ccmanager
  - overview
parent: "[[README]]"
---

# ccmanager - 개요

> [[README|목차로 돌아가기]]

---

## 1. What - ccmanager란?

> **한 줄 정의**: tmux 없이 8+ AI 코딩 에이전트를 PTY 기반으로 관리하는 TUI 세션 매니저

### 핵심 개념

ccmanager는 Claude Code, Codex, Gemini CLI 등 8종 이상의 AI 코딩 에이전트를 하나의 TUI에서 관리하는 도구다. tmux에 의존하지 않고 자체 PTY(Pseudo-Terminal)로 에이전트 세션을 생성하며, 각 에이전트의 상태(idle/busy/waiting)를 실시간으로 감지한다. `process.env`를 그대로 전달하므로 **Claude Code OAuth, Skills, Hooks, CLAUDE.md 등 고유기능이 100% 보존**된다.

### 지원 에이전트 (8종)

| 에이전트 | 명령어 | 상태 감지 |
|----------|--------|----------|
| **Claude Code** (기본) | `claude` | ✅ 전용 detector |
| **Gemini CLI** | `gemini` | ✅ 전용 detector |
| **Codex** (OpenAI) | `codex` | ✅ 전용 detector |
| **Cursor Agent** | `cursor-agent` | ✅ 전용 detector |
| **Copilot CLI** (GitHub) | `copilot` | ✅ 전용 detector |
| **Cline CLI** | `cline` | ✅ 전용 detector |
| **OpenCode** | `opencode` | ✅ 전용 detector |
| **Kimi CLI** | `kimi` | ✅ 전용 detector |

### Claude Code 고유기능 보존

실제 `claude` CLI를 PTY에서 그대로 실행하므로:

- **OAuth**: ✅ (`process.env` 패스스루)
- **CLAUDE.md**: ✅ (worktree의 `cwd`에서 자동 읽기)
- **Skills**: ✅ (풀 인터랙티브 TUI 동작)
- **Hooks**: ✅ (네이티브 동작)
- **MCP 서버**: ✅ (유저 설정 그대로)
- **Session 데이터**: worktree 간 `~/.claude/projects/` 복사 가능

> 유일한 변경: `--teammate-mode in-process` 자동 주입 (Agent Teams 충돌 방지). 직접 `--teammate-mode` 지정 시 오버라이드 가능.

### 동작 방식

```
ccmanager (TUI)
├── Session 1: claude (PTY)     [busy]
│   └── git worktree: .worktrees/feat-auth
├── Session 2: codex (PTY)      [idle]
│   └── git worktree: .worktrees/feat-api
├── Session 3: gemini (PTY)     [waiting_input]
│   └── git worktree: .worktrees/fix-bug
└── 상태 변경 → hook 실행 (알림, 로깅 등)
```

---

## 2. Why - 왜 ccmanager인가?

### Claude Squad와의 차이

| 비교 | Claude Squad | ccmanager |
|------|-------------|-----------|
| 의존성 | tmux 필수 | tmux 불필요 (자체 PTY) |
| 상태 감지 | 없음 | 실시간 idle/busy/waiting |
| 에이전트 수 | 5종 | 8종 |
| 멀티 프로젝트 | 단일 repo | `--multi-project` 지원 |
| devcontainer | 미지원 | 컨테이너 내 실행 지원 |

---

## 3. 핵심 특징

### 장점

- **8종 에이전트 지원**: Claude + Codex + Gemini 3종 모두 포함
- **tmux 불필요**: 자체 PTY — 의존성 최소화
- **실시간 상태 감지**: 에이전트별 전용 detector로 idle/busy/waiting 표시
- **Auto Approval (실험)**: Claude Haiku로 안전한 프롬프트 자동 승인
- **Status Hook**: 상태 변경 시 커스텀 명령 실행 (슬랙 알림 등)
- **Worktree Hook**: worktree 생성 후 자동 명령 (npm install 등)
- **멀티 프로젝트**: 여러 git repo를 하나의 인터페이스에서
- **devcontainer 통합**: 컨테이너 내에서 에이전트 실행
- **무료 (MIT)**: 활발한 개발 (v4.0.4, 2026-03-28)

### 단점

- **GUI 없음**: TUI 전용
- **비용 추적 없음**: Agent Deck 대비
- **Best-of-N 없음**: Emdash 대비
- **macOS/Linux만**: Windows 미지원

---

## 4. 설치 및 사용

```bash
# 설치
npm install -g ccmanager

# 또는 npx로 바로 실행
npx ccmanager

# 멀티 프로젝트 모드
CCMANAGER_MULTI_PROJECT_ROOT="/path/to/projects" ccmanager --multi-project
```

설정: `~/.config/ccmanager/config.json` 또는 프로젝트별 `.ccmanager.json`

---

## 5. 개발 현황

| 항목 | 값 |
|------|-----|
| 버전 | v4.0.4 (2026-03-28) |
| Stars | ~970 |
| 라이선스 | MIT |
| 언어 | TypeScript (Bun) |
| 메인 개발자 | kbwo (515 commits) |

---

## References

- [GitHub](https://github.com/kbwo/ccmanager)
