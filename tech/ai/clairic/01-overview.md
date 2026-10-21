---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Clairic overview

## What

Clairic은 Cloudflare Workers AI의 `@cf/cloudflare/clairic` 모델이다. free-form text를 생성하는 대신 `state`(원문)와 schema를 받아 `text`, `number`, `date`, `time`, `datetime`, `duration`, `list`, `estimate`, `forecast` 같은 bounded typed value를 반환한다. 입력은 text와 선택적 image 최대 4개를 받을 수 있다.

## Why

일반적인 LLM extraction은 JSON 생성 후 parsing, schema validation, repair/retry가 뒤따른다. field 수가 늘면 output token과 latency도 늘어난다. Clairic은 값 자체를 decode하므로 이 후처리를 줄이고, 누락된 값은 `null`로 표현할 수 있다.

## 특징

| 항목 | 동작 | 운영상 의미 |
| --- | --- | --- |
| Source span | `text`/`list`에 source character offset 제공 | 원문 highlight와 audit trail 구성 |
| Uncertainty | scalar에 `confidence`, `p_null`, `guess` | 자동 승인 대신 review/fallback routing 기준 |
| Estimate/forecast | median 및 80% interval(`p10`~`p90`), 선택 시 99 quantile | 점 추정만 보지 않고 불확실성 표시 |
| Decode | token-by-token generation 없이 single forward pass의 병렬 typed decode | field 증가에 따른 generation 부담 완화 |
| Scale | 한 pass에 안 들어가는 field는 parallel pass로 분할 | schema를 작고 독립적인 단위로 설계 |

## 배포와 상태

- 호출: Workers binding의 `env.AI.run("@cf/cloudflare/clairic", …)` 또는 REST `/ai/run/@cf/cloudflare/clairic`
- context window: 65,536 tokens, Vision 지원
- 공개 상태: 2026-10-19 Preview로 출시된 hosted API이며 open weights는 향후 계획으로만 언급됨
- 가격: input 1M tokens당 $0.10, output token 과금 없음(공식 pricing을 배포 시점에 재확인)

## 핵심 원칙

`confidence`와 interval은 사실 여부를 보장하지 않는다. 낮은 confidence뿐 아니라 고영향 field, `p_null`이 높은 값, span이 부자연스러운 결과를 review 대상으로 삼고, ground truth corpus로 schema·threshold를 검증한다.

## Sources

- https://developers.cloudflare.com/workers-ai/models/clairic/
- https://developers.cloudflare.com/changelog/post/2026-10-19-clairic-workers-ai/
- https://blog.cloudflare.com/clairic-extraction-model/
