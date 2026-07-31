---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# OmniRoute

> **한 줄 정의**: 여러 LLM provider·subscription account·API key·local model을 하나의 OpenAI-compatible `/v1/*` endpoint로 통합하고, 비용·quota·health·latency에 따라 routing과 fallback을 수행하는 MIT-licensed self-hosted AI gateway.

## Overview

OmniRoute는 AI client와 여러 upstream provider 사이에 두는 local-first gateway다. OpenAI, Anthropic, Gemini 계열 API 차이를 정규화하고, 같은 provider의 여러 account와 서로 다른 model을 하나의 routing pool로 다룬다.

```text
IDE / Agent / Application
          │ OpenAI·Anthropic·Gemini-compatible request
          ▼
    OmniRoute /v1/*
          │
          ├─ Auth / Guardrails / Compression
          ├─ Request normalization
          ├─ Combo / Auto routing
          ├─ Quota preflight / Circuit breaker
          ├─ Account / Model fallback
          └─ Usage / Cost / Latency telemetry
          │
          ▼
OAuth account │ API-key provider │ OpenAI-compatible node │ Local model
```

핵심 차별점은 API key뿐 아니라 Claude Code, Codex, Gemini CLI 같은 OAuth 기반 subscription account를 routing target으로 취급한다는 점이다. `model: "auto"`를 사용하면 연결된 provider·account를 후보로 virtual combo를 만들고 health, quota, cost, latency 등을 바탕으로 요청별 target을 선택한다.

> [!NOTE]
> 조사 기준은 2026-07-31이며, 이 노트의 OmniRoute는 PHP router 등 동명 프로젝트가 아니라 [`diegosouzapw/OmniRoute`](https://github.com/diegosouzapw/OmniRoute)다. README의 “290+ providers, 90+ free-tier providers, 500+ models, 19 strategies”는 프로젝트 측 집계이며 독립 검증 수치가 아니다. 빠른 release cadence 때문에 실제 수는 설치한 version에서 다시 확인한다.

## Learning Path

- [ ] [[01-overview|1. Overview — What, Why, architecture]]
- [ ] [[02-ecosystem|2. Ecosystem — alternatives와 선택 기준]]
- [ ] [[03-references|3. References — 공식 문서 지도]]
- [ ] [[04-learning/01-getting-started|4. Getting Started — 설치, 연결, 첫 호출]]
- [ ] [[04-learning/02-deep-dive|5. Deep Dive — routing, resilience, security]]
- [ ] [[05-projects|6. Projects — 단계별 실전 과제]]
- [ ] [[cheatsheet|7. Cheatsheet — endpoint, model, 운영 점검]]

## When To Use

- 개인 또는 소규모 팀이 여러 coding subscription, API key, free tier를 하나의 endpoint로 묶을 때
- Claude Code, Codex, Cursor 같은 client 설정을 유지하면서 upstream을 자동 전환할 때
- SaaS gateway에 모든 credential과 traffic을 맡기지 않고 local machine 또는 VPS에서 운영할 때
- 최저 비용보다 quota continuity, 즉 agent workflow가 끊기지 않는 것이 중요할 때
- Combo, Auto-Combo, MCP/A2A, memory, compression을 한 runtime에서 실험할 때
- 단일 node와 SQLite 중심의 간단한 self-hosted 구성이 workload 규모에 맞을 때

## When Not To Use

- 엄격한 enterprise SLA, vendor support, 검증된 multi-tenant isolation이 필수일 때
- Kubernetes-native horizontal scaling과 매우 높은 throughput이 핵심 요구사항일 때
- unofficial web wrapper, cookie session, TLS fingerprinting을 조직 정책상 허용할 수 없을 때
- HIPAA, 금융, 공공 환경처럼 외부 audit와 formal compliance 증명이 필요한 production system
- gateway 운영, credential rotation, upstream 약관 검토를 담당할 owner가 없을 때

> [!WARNING]
> “Local-first”는 gateway와 credential DB가 local이라는 뜻이다. 외부 provider를 선택하면 prompt와 output은 해당 upstream으로 전달된다. 또한 `STORAGE_ENCRYPTION_KEY`를 설정하지 않으면 SQLite의 민감 정보가 plaintext passthrough mode로 저장된다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/litellm/README|LiteLLM]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/ai/agent-orchestration/README|Agent Orchestration]]

## Sources

- https://github.com/diegosouzapw/OmniRoute
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/architecture/ARCHITECTURE.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/routing/AUTO-COMBO.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/SECURITY.md

