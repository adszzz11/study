---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview

## What

T3 Code는 여러 AI coding harness를 한 server와 UI 아래에서 운영하는 control plane이다. 2026년 기준 공식 지원 표면에는 Claude Code, Codex, Google Antigravity, OpenCode, Cursor, Grok이 포함되며, thread마다 provider 또는 model을 바꿀 수 있다.

이는 agent 자체를 대체하지 않는다. T3 Code server가 로컬 host에서 각 provider harness를 실행하고, client는 그 실행 상태와 대화를 조작한다. 기존 Codex 또는 Claude Code login을 재사용할 수 있는 구조다.

## Why

여러 agent를 쓰면 CLI와 인증 방식, chat history, working directory, Git branch가 제각각이 된다. 병렬 작업이 많아질수록 파일 충돌과 어떤 변경이 어느 task의 결과인지 추적하는 비용도 커진다.

T3 Code는 다음 흐름을 한곳에 모은다.

```text
task → thread → branch/worktree → agent 실행 → diff review → commit/push → PR
```

## 핵심 특징

| 영역 | 기능 | 실무상 의미 |
|---|---|---|
| Provider | 기존 subscription/login 연결 | token을 다시 판매하는 계층 없이 harness를 선택 |
| Client | Electron, local web, iOS/Android | 실행 host와 관찰 device를 분리 |
| Thread | 대화·task·context의 작업 단위 | task별 상태와 지시를 분리 |
| Workspace | branch와 Git worktree 연결 | 병렬 변경의 파일 충돌과 branch 혼선을 감소 |
| Context | file, image, terminal excerpt, PR, 다른 thread 첨부 | 긴 작업의 입력을 명시적으로 구성 |
| Git/PR | diff 검토와 여러 forge 연동 | 코드 변경을 reviewable artifact로 전환 |
| Permissions | thread별 권한 모드 | automation 범위를 task 위험도에 맞춤 |

## 권한 모드의 출발점

`Supervised → Auto-accept edits → Auto → Full access` 순으로 자율성이 커진다. 초기 기본값이 Full access일 수 있으므로, 새 repository나 팀 repository에서는 `Supervised` 또는 `Auto`에서 시작하고 승인 범위를 기록하는 편이 안전하다.

## 관련 학습

- [[tech/devtools/t3-code-control-plane/README|T3 Code]]
- [[tech/devtools/t3-code-control-plane/04-learning/02-deep-dive|심화: 운영 경계와 context]]
- [[tech/devtools/t3-code-control-plane/03-references|References]]

## Sources

- https://t3.codes/
- https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-codex.md
- https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md
