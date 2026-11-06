---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# T3 Code

> **한 줄 정의**: T3 Code는 Claude Code, Codex, Cursor, OpenCode 같은 기존 AI coding agent를 한 UI에서 실행·병렬 관리·원격 제어하는 오픈소스 agent control plane이다.

## Overview

T3 Code는 새 모델이나 token reseller가 아니라, 이미 로그인한 provider subscription을 재사용하는 BYOS(Bring Your Own Subscription) 운영 계층이다. 하나의 host machine에서 agent harness, thread, context, Git workspace를 관리하고 desktop·web·mobile client로 이를 관찰하거나 조작한다.

핵심 단위는 `thread`다. 독립 작업은 별도 branch와 Git worktree에 연결해 실행하고, 결과 diff를 검토한 뒤 commit, push, PR까지 이어간다. 따라서 여러 provider를 함께 쓸 때 생기는 terminal, 인증, 작업 디렉터리, 대화 기록의 분산을 줄인다.

```text
Desktop / Web / Mobile client
            │
      T3 Code server
  ┌─────────┼──────────┐
Thread + context   Git/worktree   T3 Connect
  │                  │                │
Codex / Claude / Cursor / OpenCode / Grok / Antigravity
```

## Learning Path

- [ ] [[tech/devtools/t3-code-control-plane/01-overview|Overview]] — control plane의 역할과 핵심 기능을 이해한다.
- [ ] [[tech/devtools/t3-code-control-plane/02-ecosystem|Ecosystem]] — coding harness 및 IDE 대안과 비교한다.
- [ ] [[tech/devtools/t3-code-control-plane/04-learning/01-getting-started|시작하기]] — 안전한 첫 thread와 worktree 실습을 수행한다.
- [ ] [[tech/devtools/t3-code-control-plane/04-learning/02-deep-dive|심화]] — context, 권한, 원격 운영 설계를 익힌다.
- [ ] [[tech/devtools/t3-code-control-plane/05-projects|Projects]] — 실제 팀·원격 개발 적용안을 설계한다.
- [ ] [[tech/devtools/t3-code-control-plane/cheatsheet|Cheatsheet]] — 작업 전 빠른 점검표로 사용한다.
- [ ] [[tech/devtools/t3-code-control-plane/03-references|References]] — 공식 문서와 원문을 확인한다.

## When To Use

- Codex와 Claude Code처럼 서로 다른 harness를 같은 repository에서 운영할 때
- 독립 task를 worktree별로 병렬 실행하고 branch/diff/PR 단위로 합칠 때
- host machine의 긴 실행을 노트북이나 mobile에서 승인·관찰·steer할 때
- provider별 결과나 tool behavior를 같은 task로 비교할 때

## When Not To Use

- 단일 IDE agent만 간단히 사용하는 개인 작업일 때
- host machine을 계속 켜 두거나 remote access를 운영할 수 없을 때
- 민감한 repository에서 권한 모드와 접근 정책을 검토할 사람이 없을 때
- 모델 선택·비용 최적화가 주 문제일 때 — T3 Code는 model gateway가 아니다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/task-observer/README|Task Observer]]

## Sources

- https://t3.codes/
- https://github.com/pingdotgg/t3code
- https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md
- https://github.com/pingdotgg/t3code/blob/main/docs/user/thread-sidebar.md
