---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenAI Codex Overview

[[tech/devtools/openai-codex-agent/README|OpenAI Codex 학습 노트]]의 개요다.

## What

Codex는 repository context와 자연어 목표를 결합해 coding task를 수행하는 agentic environment다. `openai/codex`는 Apache-2.0 라이선스의 공개 terminal agent이며, Rust 중심의 `codex-rs`, CLI, SDK 디렉터리로 구성된다.

Interactive TUI로 사람과 함께 일할 수 있고, `codex exec`로 CI나 반복 automation에 연결할 수 있다. 제품 경험은 CLI만이 아니라 IDE extension, cloud agent, code review, MCP·plugin integration까지 확장된다.

## Why

일반 completion은 다음 token이나 작은 code fragment를 제안하지만, 개발자는 여전히 파일을 찾고, 수정하고, command를 실행하고, 실패 원인을 해석한다. Codex의 목표는 이 과정을 하나의 feedback loop로 압축하는 것이다.

```text
goal → repository 탐색 → 계획/patch → shell·test 실행
     ↑                                  ↓
     └──────── 결과 관찰·수정 ───────────┘
```

## 특징

- **Instruction hierarchy**: 가까운 위치의 `AGENTS.md`에 style, build/test, 수정 금지 영역을 기록해 행동을 제한한다.
- **Tool use**: 파일 탐색, patch, shell command, Git diff와 test 결과를 다음 판단의 근거로 쓴다.
- **Safety boundary**: sandbox, filesystem permission, approval, network policy를 분리한다.
- **Extension surface**: MCP, Skills, plugins, IDE, GitHub/PR workflow, remote environment를 연결한다.
- **개발 작업공간화**: 2026 방향성은 computer use, in-app browser, SSH devbox, persistent memory, scheduled automation까지 포함한다.

## 핵심 한계

Agent가 command output이나 repository 내 문서를 신뢰할 수 없는 instruction으로 잘못 해석할 수 있다. 따라서 untrusted codebase에서는 network를 끄고 권한을 좁히며, 변경 diff와 검증 결과를 사람이 확인해야 한다.

## Next

[[tech/devtools/openai-codex-agent/04-learning/01-getting-started|시작하기]]에서 read-only 탐색부터 실습하고, 도구 선택은 [[tech/devtools/openai-codex-agent/02-ecosystem|Ecosystem]]에서 비교한다.

## Sources

- https://github.com/openai/codex
- https://learn.chatgpt.com/docs/codex/cli
- https://openai.com/index/introducing-upgrades-to-codex/
