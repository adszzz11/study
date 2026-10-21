---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Jcode — 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

## Goal

작은 repository에서 provider를 연결하고, instruction loading과 **분석 → 수정 → 실제 test** verification loop를 확인한다.

## Install and Authenticate

macOS/Linux에서는 다음 설치 방식을 제공한다. script 실행 전 URL과 조직의 package-install policy를 확인한다.

```sh
curl -fsSL https://jcode.sh/install | bash
cd <repository-root>
jcode
```

Homebrew 설치도 지원한다. 시작 후 provider를 연결하고 model과 reasoning level을 바꿔 본다.

```sh
jcode login --provider openai
# 또는 claude, gemini
# TUI 안에서: /model, /effort
```

## First Verification Loop

1. repository root의 `AGENTS.md`에 build/test command와 coding convention을 짧고 명확히 쓴다.
2. 작은 failing test 하나를 준비하거나 기존 failure를 선택한다.
3. agent에 “실패 원인을 분석하고, 최소 수정 후 test를 실행해 결과를 보고하라”고 요청한다.
4. `/test`, `/review`, `/diff`, `/todos`로 주장·diff·실행 결과를 분리해 검토한다.
5. command, exit code, 실패 로그, 변경 파일을 기록한다.

## Two-session Exercise

두 session에 겹치지 않는 task를 배분한 뒤 `/swarm`과 파일 변경 알림을 관찰한다. 동일 파일을 자주 바꿀 가능성이 있으면 worktree 또는 명시적인 file ownership으로 먼저 분할한다.

## Checklist

- [ ] provider 인증과 모델 선택을 확인했다.
- [ ] `AGENTS.md`의 build/test 규칙을 agent가 따르는지 확인했다.
- [ ] 수정 전후 test command와 exit code를 기록했다.
- [ ] `/diff`와 `/review`로 변경을 별도 검토했다.
- [ ] 병렬 작업의 파일 ownership 또는 worktree를 정했다.

## Sources

- https://jcode.sh/docs
- https://jcode.sh/docs/commands
- https://github.com/1jehuang/jcode
