---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev

> **한 줄 정의**: Jev는 TypeSafe AI의 early-access **System One model**로, 자유 텍스트 대신 입력 `state`에 대한 typed `Choice`·`Score`·`Noul` 결정을 확률과 함께 반환하는 software-native AI API다.

## Overview

Jev는 “unstructured state in, typed probabilistic decision out”을 목표로 한다. LLM의 생성 결과를 JSON으로 parse·validate하는 흐름 대신, application이 정의한 action space 안에서 routing, triage, scoring, guardrail 같은 smart if-statement를 만든다.

```text
state (text / JSON) ──► Jev questions ──► Choice / Score / Noul
                                              │
                                  policy · authorization · action
                                  (일반 application code가 소유)
```

2026-09-20 기준 2026-09-15 공개된 early access다. TypeSafe가 주장하는 70–500ms latency와 가격은 도입 근거가 아니라 검증 가설로 취급하고, 실제 domain log로 accuracy·calibration·fallback을 평가한다.

## Learning Path

- [ ] [[01-overview|1. Overview — What, Why, primitives]]
- [ ] [[02-ecosystem|2. Ecosystem — alternatives와 선택 기준]]
- [ ] [[03-references|3. References — 공식 문서와 SDK]]
- [ ] [[04-learning/01-getting-started|4. Getting Started — 첫 decision call]]
- [ ] [[04-learning/02-deep-dive|5. Deep Dive — confidence, policy, evaluation]]
- [ ] [[05-projects|6. Projects — 적용 과제]]
- [ ] [[cheatsheet|7. Cheatsheet — API와 운영 점검]]

## When To Use

- 선택지와 rubric이 미리 정해진 routing, classification, risk scoring, guardrail
- low-latency decision loop에서 확률·confidence를 policy input으로 쓸 때
- 생성 LLM, rule engine, human review 중 어느 path로 보낼지 결정할 때
- 여러 atomic question을 같은 `state`에 병렬 평가해 workflow를 제어할 때

## When Not To Use

- 사용자에게 보여 줄 prose, code, 긴 explanation을 생성해야 할 때
- option을 사전에 정의할 수 없거나 open-ended discovery가 핵심일 때
- 긴 multi-step reasoning과 tool execution 자체를 모델에 맡길 때
- 자체 labeled log·threshold·fallback을 평가할 수 없는 high-stakes 자동화

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/omniroute/README|OmniRoute]]

## Sources

- https://docs.typesafe.ai/introduction
- https://docs.typesafe.ai/primitives
- https://docs.typesafe.ai/confidence
- https://typesafe.ai/blog/introducing-system-one-models-and-jev
- https://openrouter.ai/typesafe/jev-1.13/
