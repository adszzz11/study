---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Clairic tool study

> **한 줄 정의**: Clairic은 Cloudflare Workers AI의 Preview `System One` extraction model로, 비정형 text·image에서 schema에 맞는 typed value를 단일 pass로 추출·계산·추정·예측한다.

## Overview

Clairic은 LLM이 JSON을 생성한 뒤 parse·validation·retry하는 흐름 대신, `state`와 field schema로 값 자체를 decode한다. invoice amount·due date·contact list처럼 정형 결과가 필요한 대량 문서 처리에 맞는다.

- `text`와 `list`는 원문 character offset(span)을 반환해 근거를 검토할 수 있다.
- scalar 값에는 `confidence`, `p_null`, `guess`가 포함될 수 있다.
- Workers binding 또는 REST endpoint로 호출하며, 2026-10 기준 hosted Preview다.

## Learning Path

- [ ] [01-overview](./01-overview.md)에서 System One extraction의 목적과 제약을 이해한다.
- [ ] [04-learning/01-getting-started](./04-learning/01-getting-started.md)로 invoice schema를 만들어 `env.AI.run()`을 호출한다.
- [ ] `text` span과 `confidence`/`p_null`로 human-review queue를 설계한다.
- [ ] [04-learning/02-deep-dive](./04-learning/02-deep-dive.md)에서 uncertainty, code fallback, observability를 검토한다.
- [ ] [02-ecosystem](./02-ecosystem.md)으로 Clef·generative LLM·OCR/rules의 경계를 비교한다.
- [ ] [05-projects](./05-projects.md) 중 하나를 작은 corpus와 ground truth로 평가한다.

## When To Use

- email, OCR text, PDF/image에서 bounded field를 대량 추출하고 원문 근거를 함께 남길 때
- JSON generation 비용·latency·형식 오류를 줄이면서 typed output을 소비할 때
- extraction → decision → response로 분리한 `Clairic → Clef → LLM` pipeline을 구성할 때

## When Not To Use

- 장기 multi-step arithmetic 또는 대규모 table aggregation: line item을 추출한 뒤 application code로 계산한다.
- 정밀 장기 forecast: 전용 time-series model을 backtest해 선택한다.
- 정책 해석, 복합 reasoning, 긴 사용자 응답 생성: GPT·Claude·Gemini 같은 generative LLM을 사용한다.
- 문서 형식이 매우 고정되고 예외가 적음: OCR + regex + rules가 더 단순하고 결정적일 수 있다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/mark-it-down/README|MarkItDown]]

## Sources

- https://developers.cloudflare.com/workers-ai/models/clairic/
- https://developers.cloudflare.com/changelog/post/2026-10-19-clairic-workers-ai/
- https://blog.cloudflare.com/clairic-extraction-model/
- https://developers.cloudflare.com/workers-ai/platform/pricing/
