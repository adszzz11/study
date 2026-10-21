---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Jcode

> **한 줄 정의**: Jcode는 Rust로 구현된 오픈소스 terminal AI coding-agent harness로, 저자원 다중 agent 실행과 daemon 기반 세션 협업에 초점을 둔다.

## Overview

Jcode는 model 자체보다 tool, context, memory, verification loop, session 관리가 개발 결과를 좌우한다는 문제의식에서 출발한 runtime이다. daemon이 session·provider 호출·tool 실행을 소유하고, Rust TUI client가 Unix socket으로 연결한다. 따라서 같은 repository에서 여러 agent를 병렬로 운용하거나 원격 host의 긴 build/test 작업에 다시 접속하기 좋다.

기준일은 **2026-10-21**이며, 공개 release는 `v0.98.1`(2026-10-15)까지 확인한다. RAM·startup·benchmark 수치는 프로젝트가 직접 공개한 결과이므로, 도입 전에는 자신의 repository, model, OS, concurrency로 재현한다.

## Learning Path

- [ ] [[01-overview|개요]] — What/Why와 architecture 파악
- [ ] [[02-ecosystem|생태계]] — Claude Code, Codex CLI, OpenCode, Pi와 비교
- [ ] [[03-references|참고자료]] — 공식 문서·release·source 확인
- [ ] [[04-learning/01-getting-started|시작하기]] — 설치, provider login, 첫 verification loop
- [ ] [[04-learning/02-deep-dive|심화]] — swarm, memory, MCP, SDK와 security boundary
- [ ] [[05-projects|프로젝트]] — 병렬 triage, migration, remote host 자동화 적용
- [ ] [[cheatsheet|치트시트]] — command와 안전 점검 빠른 참조

## When To Use

- 동일 host/repository에서 독립적인 조사·수정·검증 작업을 여러 agent에 나눌 때
- 장시간 build/test를 daemon session으로 유지하고 local TUI에서 재접속할 때
- Claude, OpenAI/Codex, Gemini, local model 등 provider를 한 harness에서 비교할 때
- MCP, `AGENTS.md`, `SKILL.md`, TypeScript SDK를 연결해 반복 workflow를 자동화할 때

## When Not To Use

- 한 agent의 짧고 단순한 편집만 필요해 session orchestration 비용이 더 클 때
- 성능 주장만 보고 workload별 evaluation 없이 toolchain을 표준화할 때
- 신뢰할 수 없는 repository, prompt, MCP를 host 권한으로 곧바로 실행할 때
- 여러 agent가 같은 파일을 빈번하게 동시에 고치는 작업을 ownership/worktree 분리 없이 수행할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — agent tool 연결의 권한 경계

## Sources

- https://jcode.sh/
- https://jcode.sh/docs
- https://github.com/1jehuang/jcode
- https://jcode.sh/releases
- https://jcode.sh/sdk
