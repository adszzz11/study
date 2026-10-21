---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive: uncertainty, evidence, and boundaries

## Span 기반 review UX

`text`와 `list`의 source character offset을 원문 viewer의 highlight로 변환한다. reviewer에게는 추출 값만 보여주지 말고 다음을 같이 제공한다.

- 원문 snippet과 강조된 span
- field instruction 및 schema version
- `confidence`, `p_null`, `guess`
- model ID, request ID, 입력 문서 식별자

offset은 OCR 정규화·공백 치환 후 원문과 달라질 수 있다. extraction에 보낸 정확한 `state`를 보존하고, viewer가 같은 문자열을 기준으로 offset을 해석하도록 한다.

## Estimate와 forecast

`estimate`/`forecast`에는 `min`, `max`, `step`, `scale`처럼 허용 범위를 선언하고, median(`p50`)뿐 아니라 `p10`~`p90` interval을 UI와 policy에 표시한다. 필요하면 99개 quantile을 요청한다.

```text
예: estimated loss = p50 1,200 USD
    80% interval = 800–1,800 USD
```

이 interval은 자동 결정의 정답 보증이 아니다. alert triage 같은 보조 신호로 사용하고, 실제 시계열 forecast는 held-out 기간의 backtest로 전용 model과 비교한다.

## Arithmetic과 aggregation 분리

Clairic에는 line item의 description·quantity·unit price를 추출하게 하고, 합계와 tax 계산은 decimal-safe application code로 재계산한다.

```ts
const recomputed = lines.reduce(
  (sum, line) => sum.plus(line.quantity).times(line.unitPrice),
  new Decimal(0),
);
const mismatch = !recomputed.equals(extractedTotal);
```

금융 금액은 floating-point 오차를 피할 수 있는 decimal library 또는 최소 화폐 단위 integer를 사용한다. 원 추출값과 계산값이 다르면 자동 적재하지 말고 review로 보낸다.

## Observability와 rollback

AI Gateway를 연결해 request log, input token 비용, latency, error/retry, cache policy를 관찰한다. rollout은 schema version별로 진행한다.

1. shadow mode: 기존 workflow와 병렬 실행하고 결과만 비교한다.
2. review-only: Clairic 결과가 reviewer 화면에만 나타나도록 한다.
3. limited write: 낮은 위험 document type부터 write 권한을 연다.
4. rollback: schema/model routing을 이전 version으로 되돌리고, 잘못 적재된 record를 audit log로 식별한다.

## Sources

- https://developers.cloudflare.com/workers-ai/models/clairic/
- https://developers.cloudflare.com/ai-gateway/observability/
- https://developers.cloudflare.com/changelog/post/2026-10-19-clairic-workers-ai/
