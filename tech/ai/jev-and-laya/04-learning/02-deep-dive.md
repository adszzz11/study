---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev와 laya Deep Dive

> [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. 판단을 합성하고, 모델에 정책을 맡기지 않는다

Jev의 질문은 같은 state에 대해 병렬·독립적으로 평가할 수 있다. 복합 판단을 한 문장으로 묻기보다 작은 결과를 application code에서 합성한다.

```python
def route(decision):
    department = decision["department"]
    urgent = decision["urgency"]
    refund = decision["refund_request"]

    if refund["noul"] >= 0.9:
        return "refund-review"  # 환불 실행이 아니라 review queue
    if department["confidence"] >= 0.85 and urgent["score"] < 2:
        return f"auto-route:{department['choice']}"
    return "human-escalation"
```

실제 property와 response shape은 선택한 SDK/version에서 확인한다. 위 예시는 policy separation을 보이기 위한 pseudocode다.

## 2. confidence와 probability

Jev의 `Choice`/`Score` `confidence`는 probability distribution 집중도의 요약값이다. 즉 “정답 확률 0.85”와 동일한 의미로 가정하지 않는다. `Noul`에는 `confidence`가 없으므로 yes probability를 domain threshold와 함께 해석한다.

권장 시작 정책:

| 구간 | 동작 | 전제 |
|---|---|---|
| `>= 0.85` | low-risk 자동 처리 후보 | held-out data에서 검증 |
| 중간 구간 | review queue 또는 추가 정보 요청 | reviewer SLA 측정 |
| 낮은 구간 | human escalation 또는 reasoning LLM fallback | 무리한 추측 금지 |

`0.85`는 학습용 예시다. destructive action에는 더 높은 threshold와 사용자 확인을 둔다.

## 3. laya calibration과 boundary test

laya README는 base checkpoint의 typed-decision zero-shot 한계와 calibration 필요성을 명시한다. production 전에 최소한 다음 slice를 분리해 평가한다.

- 각 class와 rare class, 50개 이상 choice option
- negation·ambiguous wording·빈 입력·중복 입력
- language별 routing 결과와 code-switching text
- long input의 truncation 및 `max_len` 변화
- false positive/negative의 business cost

온도 보정은 validation split에서만 fit하고, test split은 마지막 보고에 남긴다. test data로 threshold를 반복 조정하면 evaluation이 낙관적으로 치우친다.

## 4. Offline evaluation 설계

```text
historical examples
  ├─ train / calibration split
  ├─ validation: temperature + threshold 선택
  └─ held-out test: accuracy, ECE, coverage, review rate
```

| 지표 | 질문 |
|---|---|
| Accuracy / macro-F1 | class imbalance에서도 맞는가? |
| Coverage | 자동 처리 대상이 얼마나 되는가? |
| ECE | reported probability가 실제 정답률과 맞는가? |
| Review rate | 운영 인력이 감당 가능한가? |
| Cost-weighted error | 잘못된 auto-action이 얼마나 비싼가? |

## 5. 안전한 cascade

```text
typed decision
   ├─ high confidence + low-risk policy → bounded auto-action
   ├─ medium confidence → review / request clarification
   └─ low confidence or complex case → reasoning LLM or human
```

생성형 LLM fallback도 final authority가 아니다. `delete`, `refund`, external message와 같은 side effect에는 idempotency, audit log, authorization, explicit confirmation을 별도로 둔다.

## Sources

- https://docs.typesafe.ai/confidence
- https://github.com/NandhaKishorM/laya
- https://github.com/NandhaKishorM/laya/blob/main/BENCHMARKS.md
