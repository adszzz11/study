---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Clairic cheatsheet

## Model and call

```ts
const result = await env.AI.run("@cf/cloudflare/clairic", {
  state: sourceText,
  fields: {
    invoice_id: { type: "text", instruction: "Invoice identifier" },
    due_date: { type: "date", instruction: "Payment due date" },
    total: { type: "number", decimals: 2, unit: "currency" },
  },
});
```

실제 request/response property는 Preview API이므로 항상 [공식 schema](https://developers.cloudflare.com/workers-ai/models/clairic/)와 대조한다.

## Types

| 범주 | type |
| --- | --- |
| 원문 기반 값 | `text`, `number`, `date`, `time`, `datetime`, `duration`, `list` |
| 불확실성 포함 값 | `estimate`, `forecast` |
| 입력 | `state` text + 선택적 image 최대 4개 + field schema |

## Output을 소비하는 규칙

- `value === null`: 값을 임의로 채우지 말고 null reason/`p_null`을 기록한다.
- `confidence`: field·문서 유형별 threshold와 함께 사용한다.
- `p_null`: 누락 가능성 신호로 review/fallback 조건에 넣는다.
- span: exact input `state`를 보존해 highlight의 기준으로 삼는다.
- `p10`/`p50`/`p90`: point estimate가 아닌 interval로 사용자에게 제시한다.

## Do / Don't

| Do | Don't |
| --- | --- |
| schema를 좁고 명확한 field로 작성 | 막연한 instruction 하나에 여러 business 의미를 섞기 |
| line item 추출 후 code로 합계 검증 | 복잡한 산술·대규모 집계를 결과값 그대로 신뢰 |
| ground truth corpus로 threshold 평가 | `confidence`만으로 자동 승인 |
| Gateway log로 비용·latency·error 관찰 | Preview 동작과 가격을 고정 가정 |
| Clef/LLM과 역할 분리 | Clairic에 policy 판단이나 긴 응답 생성을 강제 |

## Sources

- https://developers.cloudflare.com/workers-ai/models/clairic/
- https://developers.cloudflare.com/workers-ai/platform/limits/
