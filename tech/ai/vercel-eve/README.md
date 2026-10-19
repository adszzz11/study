---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Vercel eve

> **한 줄 정의**: Vercel eve는 TypeScript와 filesystem-first 구조로 durable execution, sandbox, human approval, subagent, eval을 기본 내장해 production AI agent를 만드는 오픈소스 framework이다.

## Overview

eve는 LLM 호출 자체보다 production agent에 필요한 실행 기반에 초점을 둔다. `instructions.md`로 시작해 tool, connection, channel, schedule, eval을 directory 단위로 늘리며 Git에서 함께 검토할 수 있다. 각 agent loop는 durable workflow로 실행되어 crash·deployment·승인 대기 뒤에도 checkpoint부터 재개된다.

핵심 경계는 App runtime과 Sandbox의 분리다. credential과 connection client는 app runtime에 두고, shell·파일·code execution은 session별 isolated sandbox에서 수행한다. 아직 **public preview**이므로 version pinning, representative eval, staged deployment를 전제로 도입한다.

## Learning Path

- [ ] [[01-overview|개요]] — What/Why와 filesystem-first 구조 이해
- [ ] [[02-ecosystem|생태계]] — LangGraph, CrewAI, Vercel AI SDK와 비교
- [ ] [[03-references|참고자료]] — 공식 문서와 release history 확인
- [ ] [[04-learning/01-getting-started|시작하기]] — scaffold, instruction, read-only tool 실습
- [ ] [[04-learning/02-deep-dive|심화]] — durability, approval, sandbox, subagent, eval 설계
- [ ] [[05-projects|프로젝트]] — support·data analysis agent 적용
- [ ] [[cheatsheet|치트시트]] — 운영 시 빠른 참조

## When To Use

- TypeScript/Vercel 환경에서 long-running production agent를 빠르게 구성할 때
- tool 실행 격리, approval, channel 연동, eval을 하나의 runtime convention으로 운영할 때
- Slack·Web·API에서 같은 agent를 제공하고 durable session을 유지해야 할 때
- specialist subagent에 별도 tool 권한과 fresh context를 부여할 때

## When Not To Use

- 단순한 streaming chat이나 UI integration만 필요한 기존 application일 때
- 명시적인 graph와 모든 step의 세밀한 deterministic 제어가 핵심일 때
- public preview API를 pinning·eval·staged rollout 없이 장기 고정 dependency로 삼을 때
- non-idempotent write action을 approval·idempotency 없이 자동 실행하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/agent-orchestration/README|Agent Orchestration]] — agent runtime과 운영 흐름을 함께 살펴볼 맥락

## Sources

- https://vercel.com/blog/introducing-eve
- https://eve.dev/
- https://github.com/vercel/eve
- https://github.com/vercel/eve/blob/main/docs/concepts/execution-model-and-durability.mdx
