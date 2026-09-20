---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Headroom AI

> **한 줄 정의**: Headroom은 LLM/AI agent가 provider로 보내는 tool output, logs, RAG documents, files, conversation context를 content-aware 방식으로 줄이고, 필요하면 local 원문을 다시 가져오게 하는 context optimization layer다.

## Overview

Agentic workflow에서는 사람의 prompt보다 code search 결과, build logs, MCP response, API JSON 같은 machine-generated context가 더 빠르게 커진다. **Headroom AI (`headroom-ai`)**는 이런 payload를 provider 전송 전에 local에서 분류·압축해 input token, prefill latency, context-window 소비를 줄인다.

- 큰 tool-generated content에 집중하고 system prompt, user instruction, recent context는 보호한다.
- JSON, logs, search result, diff, HTML, config, code, general text에 서로 다른 compressor를 적용한다.
- **CCR(Compress–Cache–Retrieve)**로 원문을 local SQLite에 저장하고 retrieval marker를 남긴다.
- proxy, agent wrapper, Python API, TypeScript SDK, MCP server, framework adapter로 통합할 수 있다.
- proxy의 `cache` mode는 prefix cache 안정성을, `token` mode는 더 큰 token 절감을 우선한다.

> [!NOTE]
> 조사 기준일은 2026-09-20이며 dossier가 확인한 최신 정식 버전은 **v0.37.0 (2026-08-27)**이다. 절감률은 workload에 따라 크게 달라지며, coding agent에서 항상 60–95%가 절감되는 것은 아니다.

## Learning Path

- [ ] [[headroom/01-overview|01. What, Why, 핵심 특징]]
- [ ] [[headroom/02-ecosystem|02. Ecosystem과 대안 비교]]
- [ ] [[headroom/03-references|03. 공식 자료와 검증 포인트]]
- [ ] [[headroom/04-learning/01-getting-started|04-1. Getting Started]]
- [ ] [[headroom/04-learning/02-deep-dive|04-2. Deep Dive]]
- [ ] [[headroom/05-projects|05. 실습 Projects]]
- [ ] [[headroom/cheatsheet|Cheatsheet]]

## When To Use

- code search, CI/test logs, DB rows, API JSON처럼 크고 반복적인 tool output이 context 대부분을 차지할 때
- long-running coding agent에서 context window와 provider prefix cache를 함께 관리할 때
- payload를 외부 compression service에 보내지 않고 local에서 처리해야 할 때
- 압축된 항목의 원문을 필요 시 retrieval tool로 복구하는 경로가 필요할 때
- 실제 workload를 `audit` 또는 `simulate`한 뒤 token 절감 효과가 확인됐을 때

## When Not To Use

- 짧거나 이미 조밀한 context라 compression overhead와 운영 복잡성이 더 클 때
- source code, exact formatting, 모든 row처럼 원문 전체가 답변에 반드시 필요할 때
- retrieval tool 주입·실행을 보장할 수 없거나 CCR TTL/eviction이 허용되지 않을 때
- 최종 answer equivalence에 대한 강한 품질 보증이 필요한데 자체 evaluation이 없을 때
- compression 비율만 보고 정확도 저하를 감수할 수 없는 high-stakes workflow

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[litellm/README|LiteLLM]]
- [[agent-garden]]

## Sources

- https://docs.headroomlabs.ai/docs
- https://docs.headroomlabs.ai/docs/architecture
- https://docs.headroomlabs.ai/docs/how-compression-works
- https://docs.headroomlabs.ai/docs/ccr
- https://docs.headroomlabs.ai/docs/benchmarks
- https://github.com/headroomlabs-ai/headroom
- https://github.com/headroomlabs-ai/headroom/releases
- https://pypi.org/project/headroom-ai/
- https://www.npmjs.com/package/headroom-ai
