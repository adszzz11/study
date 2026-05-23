---
date: 2026-03-28
tags:
  - tech
  - claude-squad
  - overview
parent: "[[README]]"
---

# Claude Squad - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - Claude Squad란?

> **한 줄 정의**: tmux + git worktree 기반 멀티 에이전트 관리 CLI

### 핵심 개념

Claude Squad는 "하나의 터미널에서 여러 AI 에이전트를 관리"하는 도구다. 각 에이전트는 독립된 git worktree에서 실행되어 코드 충돌 없이 병렬 작업이 가능하다. tmux를 백엔드로 사용하여 세션을 관리하며, `cs` 명령어 하나로 모든 에이전트를 모니터링한다.

### 주요 용어

| 용어 | 설명 |
|------|------|
| Instance | 하나의 에이전트 세션 (worktree + tmux 세션) |
| Worktree | git worktree로 격리된 작업 디렉토리 |
| Auto-accept | 에이전트의 모든 액션을 자동 승인하는 모드 |
| Background | 에이전트를 백그라운드에서 자동 실행 |
| Diff View | 에이전트가 만든 변경사항을 diff로 확인 |

### 동작 방식

```
cs (Claude Squad CLI)
├── Instance 1: Claude Code
│   ├── tmux session: squad-1
│   └── git worktree: .worktrees/squad-1
├── Instance 2: Codex
│   ├── tmux session: squad-2
│   └── git worktree: .worktrees/squad-2
└── Instance 3: Aider
    ├── tmux session: squad-3
    └── git worktree: .worktrees/squad-3
```

---

## 2. Why - 왜 Claude Squad인가?

### 해결하려는 문제

- 여러 에이전트를 수동으로 각각 별도 터미널에서 관리하기 번거로움
- 같은 repo에서 여러 에이전트가 작업하면 충돌 발생
- 에이전트 실행 결과를 리뷰하고 머지하는 워크플로우 필요

### 기존 방식의 한계

| 문제 | 기존 방식 | Claude Squad |
|------|----------|-------------|
| 세션 관리 | 터미널 탭 수동 | cs 명령어로 통합 |
| 코드 격리 | 수동 git worktree | 자동 생성/정리 |
| 백그라운드 | nohup/screen | auto-accept 모드 |
| 결과 확인 | git diff 수동 | 내장 diff view |

---

## 3. 핵심 특징

### 장점

- **초간단 설치**: `brew install claude-squad` 한 줄
- **git worktree 자동 격리**: 에이전트 간 충돌 원천 차단
- **다중 에이전트 지원**: Claude Code, Codex, Aider, Amp, OpenCode
- **백그라운드 실행**: auto-accept 모드로 무인 실행
- **무료 오픈소스**: 활발한 커뮤니티
- **경량**: tmux 기반으로 리소스 최소 사용

### 단점

- **tmux 의존**: tmux가 설치되어 있어야 함
- **GUI 없음**: 터미널 전용 — GUI 선호 시 Conductor 추천
- **모델 라우팅 없음**: OMC 같은 비용 최적화 미제공
- **macOS/Linux**: Windows 미지원 (WSL 가능)

---

## 4. 사용 사례

### 적합한 경우

| 사용 사례 | 설명 |
|----------|------|
| 가벼운 병렬 작업 | 2-5개 에이전트를 간단히 돌리고 싶을 때 |
| 다중 에이전트 혼용 | Claude Code + Codex + Aider를 같이 쓸 때 |
| 백그라운드 작업 | 에이전트를 띄워놓고 다른 작업하면서 결과 확인 |
| CLI 워크플로우 | 터미널 중심 개발 환경에서 |

---

## 5. 가격 정책

| 플랜 | 가격 | 특징 |
|------|------|------|
| 무료 | $0 | 전체 기능 (오픈소스) |

---

## 다음 단계

> [!tip] 다음으로
> Claude Squad의 개요를 이해했다면 [[02-ecosystem|생태계와 대안 도구 비교]]를 살펴보세요.

---

## References

- [공식 사이트](https://smtg-ai.github.io/claude-squad/)
- [GitHub](https://github.com/smtg-ai/claude-squad)
