---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenAI Codex — 오픈소스 기반 Agentic Coding 환경

> **한 줄 정의**: OpenAI Codex는 terminal·IDE·cloud에서 repository를 읽고, 계획·수정·명령 실행·검증을 수행하는 Agentic Coding 제품 및 핵심 CLI 구현체다.

## Overview

기존 code completion이 코드 작성 순간을 돕는다면, Codex는 자연어 목표를 받아 **탐색 → 계획 → 구현 → tool 실행 → 결과 검토**를 반복하는 agent loop를 지향한다. 공개 repository의 Apache-2.0 CLI는 Rust 중심이며, interactive TUI와 `codex exec` 기반 automation을 모두 제공한다.

- integration: shell, Git, `AGENTS.md`, MCP, plugins, IDE extension, cloud/remote environment
- programmatic use: TypeScript SDK는 local CLI thread를, Python SDK는 local `app-server` JSON-RPC를 제어한다.
- 운영 원칙: sandbox, approval, filesystem·network 최소 권한, Git checkpoint, test verification을 함께 사용한다.

## Learning Path

- [ ] [[tech/devtools/openai-codex-agent/01-overview|Overview]] — 문제와 핵심 동작 모델
- [ ] [[tech/devtools/openai-codex-agent/02-ecosystem|Ecosystem]] — 유사 도구와의 선택 기준
- [ ] [[tech/devtools/openai-codex-agent/03-references|References]] — 공식 문서와 검증 지점
- [ ] [[tech/devtools/openai-codex-agent/04-learning/01-getting-started|시작하기]] — 안전한 첫 repository 실습
- [ ] [[tech/devtools/openai-codex-agent/04-learning/02-deep-dive|Deep Dive]] — instructions, SDK, 권한 경계
- [ ] [[tech/devtools/openai-codex-agent/05-projects|Projects]] — 적용 프로젝트 아이디어
- [ ] [[tech/devtools/openai-codex-agent/cheatsheet|Cheatsheet]] — 명령과 운영 체크리스트

## When To Use

- 여러 파일을 넘나드는 bug fix, test failure triage, migration처럼 탐색과 검증이 함께 필요한 작업
- 명확한 build/test 절차를 `AGENTS.md`로 제공할 수 있는 repository
- `codex exec`로 반복 가능한 CI·review·점검 작업을 자동화할 때
- local에서 시작한 작업을 IDE, cloud agent, remote environment로 이어 갈 때

## When Not To Use

- secret 또는 production write 권한을 최소화할 수 없는 작업
- untrusted codebase인데 sandbox·approval·network 정책을 검토하지 못한 경우
- 한 줄 수정처럼 agent loop의 탐색·검증 비용보다 직접 수정이 작은 경우
- test 또는 review 없이 생성 결과를 그대로 배포해야 하는 흐름

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/git/README|Git]]

## Sources

- https://github.com/openai/codex
- https://learn.chatgpt.com/docs/codex/cli
- https://learn.chatgpt.com/docs/codex-sdk
- https://openai.com/index/introducing-upgrades-to-codex/
- https://openai.com/index/codex-for-almost-everything/
