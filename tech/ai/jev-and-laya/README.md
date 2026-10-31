---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev와 laya

> **한 줄 정의**: Jev와 laya는 자유 텍스트 대신 `Choice`·`Score`·`Noul` 같은 typed decision과 probability를 반환해 application control-flow를 돕는 System One decision model 계열이다.

## Overview

일반 LLM이 문장을 생성한다면, Jev와 laya는 “이 ticket을 어느 팀으로 보낼까?”, “사람의 검토가 필요한가?”처럼 범위가 정해진 판단을 코드가 바로 사용할 값으로 돌려준다. Jev는 TypeSafe AI의 hosted API이고, laya는 Apache-2.0 open-weight runtime으로 self-host할 수 있다.

```text
ticket / alert / agent action
            │ state + atomic questions
            ▼
  Jev (hosted) 또는 laya (self-host)
            │ typed answer + probabilities
            ▼
auto action ── review queue ── human escalation
```

둘은 chat, 장문 reasoning, open-ended QA를 대체하지 않는다. routing, triage, moderation, guardrail, scoring에 맞는 빠른 판단 계층으로 보고, 복합·저신뢰 case는 reasoning LLM이나 사람에게 넘긴다.

## Learning Path

- [ ] [[01-overview|1. Overview — What, Why, 특징]]
- [ ] [[02-ecosystem|2. Ecosystem — 대안과 선택 기준]]
- [ ] [[03-references|3. References — 공식 문서 지도]]
- [ ] [[04-learning/01-getting-started|4. Getting Started — 첫 typed decision]]
- [ ] [[04-learning/02-deep-dive|5. Deep Dive — atomic question, confidence, evaluation]]
- [ ] [[05-projects|6. Projects — 실전 적용 과제]]
- [ ] [[cheatsheet|7. Cheatsheet — API와 운영 점검]]

## When To Use

- 선택지와 정책이 미리 정의된 ticket routing·alert triage·content moderation
- agent의 `delete`, `refund`, `send message` 전 intent/risk gate
- probability와 threshold로 human review 비율을 제어하는 workflow
- PII 또는 egress 제약 때문에 local/offline 판단 계층이 필요한 경우(laya)
- 저신뢰·복합 case만 생성형 LLM에 보내 latency와 비용을 줄이는 cascade

## When Not To Use

- 새로운 class를 즉석에서 발견하거나 긴 설명·창작이 필요한 open-ended task
- 하나의 deterministic compliance rule로 충분한 최종 승인 gate
- domain별 held-out evaluation과 threshold 운영을 할 owner가 없는 production workflow
- 중요한 행동을 모델 probability 하나만으로 즉시 실행해야 하는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/ai/litellm/README|LiteLLM]]

## Sources

- https://docs.typesafe.ai/introduction
- https://docs.typesafe.ai/introduction/quickstart
- https://docs.typesafe.ai/confidence
- https://github.com/NandhaKishorM/laya
- https://huggingface.co/convaiinnovations/laya
