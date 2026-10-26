---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive: rubric, calibration, and migration

## 좋은 question 설계

`choice` criteria는 서로 겹치지 않게 만들고, fallback option을 둔다. `score` criteria는 낮은 level에서 높은 level로 엄격히 순서가 있어야 한다. 모호한 “중요함” 대신 관찰 가능한 조건을 적는다.

```json
{
  "type": "score",
  "instructions": "Rate the incident urgency for an on-call response.",
  "criteria": [
    "Low: no user impact and no deadline within 24 hours",
    "Medium: limited user impact or a deadline within 24 hours",
    "High: broad user impact, security risk, or active outage"
  ]
}
```

## Calibration workflow

1. representative labeled data를 train/validation/test로 나눈다. question wording과 threshold는 validation에서만 튜닝한다.
2. test set에서 probability bucket별 precision/recall을 확인한다.
3. 자동화의 손실을 반영한다. secret guard는 false negative, reviewer queue는 false positive 비용도 함께 본다.
4. low-confidence 또는 threshold 근처 case는 human review로 보낸다.
5. question, model version, threshold, evaluation date를 함께 versioning한다.

확률은 decision policy의 입력값이지 보증서가 아니다. 특히 data distribution이나 rubric 정의가 바뀌면 이전 threshold는 신뢰하지 않는다.

## Local에서 hosted로 옮기기

local Flash와 hosted API는 동일한 request schema를 사용한다. hosted 전환은 endpoint를 `https://api.perplexity.ai/v1/decisions`로 바꾸고 `Authorization: Bearer ...`를 더하는 형태다. 그러나 local은 Q8 GGUF Flash runtime이고 hosted는 별도 serving deployment다. 기존 threshold를 그대로 복사하지 말고, 각 target model에서 동일 labeled sample로 다시 calibration한다.

| 조건 | Decider for Mac | hosted Decisions API |
|---|---|---|
| data residency | Mac에 머문다 | request content가 API로 전송된다 |
| 비용 | API key/usage bill 없음 | 입력 token 기준 과금 |
| 모델/scale | Flash 4B, 단일 Mac | Flash 또는 27B, 서비스 scale |
| question grouping | one question per request 권장 | 관련 question은 joint inference를 평가 가능 |

## Image와 operational safety

image `state`는 screenshot organizer나 error monitor에 쓸 수 있지만, 화면에 token·개인정보가 있을 수 있다는 전제로 접근 권한과 로그 보존 범위를 정한다. localhost라도 같은 Mac의 다른 process가 endpoint에 접근할 수 있으므로, sensitive input을 장기 로그에 남기지 않고 automation 실행 권한을 최소화한다.

## Runtime compatibility

GGUF artifact는 일반-purpose runtime의 호환성을 보장하지 않는다. protocol v3, non-causal/full-attention, marker별 readout 요구사항 때문에 일반 `llama.cpp` server로 대체하기 전에 end-to-end decision 결과를 검증해야 한다. 실용적인 기본값은 공식 Decider app이다.

## Sources

- https://docs.perplexity.ai/docs/decisions/quickstart
- https://docs.perplexity.ai/docs/decisions/decider-for-mac
- https://huggingface.co/perplexity-ai/pplx-decider-flash-gguf-v1.2
