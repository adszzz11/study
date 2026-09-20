---
date: 2026-08-15
tags: [tech]
type: tech-tool-study
status: draft
---

# NVIDIA NeMo Switchyard

> **한 줄 정의**: Switchyard는 OpenAI·Anthropic 호환 client와 여러 LLM backend 사이에서 protocol translation, intelligent model routing, fallback, session affinity, observability를 수행하는 NVIDIA의 open-source LLM traffic orchestration layer다.

## Overview

Switchyard는 application이 기대하는 API semantics와 실제 model serving endpoint를 분리한다. 요청을 provider-neutral type으로 변환한 뒤 route algorithm이 target을 선택하고, upstream 형식으로 다시 encode한다. 이를 통해 단순 작업은 efficient model로, 복잡한 추론·오류 복구는 capable model로 보낼 수 있다.

주요 구성은 다음과 같다.

- `switchyard-server`: OpenAI/Anthropic-compatible standalone Rust HTTP proxy
- `switchyard-libsy`: 다른 Rust gateway나 agent runtime에 routing algorithm을 내장하는 library
- `switchyard launch claude|codex|openclaw`: local proxy lifecycle과 coding-agent endpoint 설정을 관리하는 launcher
- `switchyard-protocol` / `switchyard-translation`: provider-neutral type과 protocol translation
- `passthrough`, `random`, `llm_classifier`, `stage_router`: 목적별 routing algorithm

> [!warning]
> 조사 기준일은 2026-08-15이며 최신 공개 버전은 v0.2.0이다. 프로젝트가 스스로 **pre-alpha**를 표방하고 PyPI classifier도 Alpha이므로 production 전면 도입보다 local experiment, shadow traffic, bounded canary로 평가하는 편이 안전하다.

## Learning Path

- [ ] [[01-overview|Overview]] — 해결하려는 문제와 native Rust architecture 이해
- [ ] [[02-ecosystem|Ecosystem]] — LiteLLM, Envoy AI Gateway, provider SDK, custom proxy와 비교
- [ ] [[03-references|References]] — release, core concepts, algorithm 문서 확인
- [ ] [[04-learning/01-getting-started|Getting Started]] — 설치, TOML 구성, health check, passthrough 검증
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — classifier, stage router, session affinity, observability 설계
- [ ] [[05-projects|Projects]] — protocol bridge와 coding-agent router 실험
- [ ] [[cheatsheet|Cheatsheet]] — endpoint, algorithm, 운영 점검표 빠른 참조

## When To Use

- OpenAI Chat Completions, OpenAI Responses, Anthropic Messages client를 여러 backend에 연결할 때
- task complexity나 agent 진행 단계에 따라 efficient/capable model을 자동 선택할 때
- Claude Code, Codex CLI 같은 coding agent의 endpoint를 OpenRouter, vLLM, Ollama, NVIDIA NIM 등으로 바꿀 때
- routing algorithm을 HTTP proxy와 분리해 Rust gateway 또는 agent runtime에 내장할 때
- 실제 serving target, token, cache, retry, latency, routing 근거를 함께 관찰할 때
- 새 routing policy를 shadow traffic이나 A/B test로 검증할 때

## When Not To Use

- pre-alpha dependency를 허용할 수 없는 mission-critical production gateway
- 단일 provider·단일 model만 호출하며 protocol translation이나 routing이 필요 없는 application
- API key, quota, tenant별 budget, enterprise governance가 핵심인데 별도 control plane을 둘 수 없는 환경
- `stage_router`의 heuristic을 검증할 trajectory log와 evaluation set이 없는 경우
- legacy Python/FastAPI, YAML bundle, `switchyard serve` 사용법을 그대로 유지해야 하는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/litellm/README|LiteLLM]] — provider gateway, load balancing, budget 관리 비교 대상
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol]] — model traffic이 아닌 agent-to-tool/data integration layer
- [[tech/ai/agent-orchestration/cli-agents|CLI Agents]] — coding-agent runtime과 launcher 적용 맥락

## Sources

- [NVIDIA NeMo Switchyard GitHub](https://github.com/NVIDIA-NeMo/Switchyard)
- [v0.2.0 Release](https://github.com/NVIDIA-NeMo/Switchyard/releases/tag/v0.2.0)
- [PyPI: nemo-switchyard 0.2.0](https://pypi.org/project/nemo-switchyard/0.2.0/)
- [Getting Started](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/getting_started.md)
- [Core Concepts](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/core_concepts.md)

