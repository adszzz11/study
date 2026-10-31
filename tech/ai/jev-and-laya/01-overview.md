---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev와 laya Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Jev와 laya는 state(판단할 텍스트 또는 구조화된 맥락)와 질문 schema를 받아 typed answer를 반환하는 System One decision model 접근이다.

| Primitive | 목적 | 예시 |
|---|---|---|
| `Choice` / `choice` | 정해진 후보 중 하나 선택 | `billing`, `technical`, `sales` |
| `Score` / `score` | 순서 있는 수준 평가 | frustration `0`–`2` |
| `Noul` / `noul` | yes/no 확률 | 환불 요청인지 |

Jev는 TypeSafe AI의 managed API다. 같은 state에 대한 여러 atomic question을 한 요청에 두고, 독립 결과를 application code가 합성하는 모델이다. laya는 Convai Innovations의 open-weight Python runtime으로, non-autoregressive encoder 기반 단일 forward pass로 typed decision을 낸다.

## Why

생성형 LLM의 JSON output은 schema validation, parsing failure, free-form 답변, hallucination 대응을 application이 다시 떠안기 쉽다. typed decision API는 그 경계를 좁힌다.

```text
free-form generation → parse → validate → policy
typed decision       → probability/confidence → policy
```

이는 판단 자체가 항상 정확하다는 뜻이 아니다. value는 출력 contract와 확률 신호를 통해 자동 실행, review, escalation의 control-flow를 명시적으로 만들 수 있다는 데 있다.

## 특징

| 항목 | Jev | laya |
|---|---|---|
| 제공 형태 | TypeSafe hosted API | open weights + Python runtime/self-host |
| 질문 | `Choice`, `Score`, `Noul` | `choice`, `score`, `noul` |
| 결과 | typed answer, probability, Choice/Score `confidence` | typed answer, probability, routing metadata |
| 실행 | 관리형 서비스, 여러 질문을 독립 평가 | non-autoregressive encoder, single forward pass |
| 공개성 | weights·세부 architecture 비공개 | Apache-2.0, checkpoint 공개 |
| 운영 | API key·network 의존 | infra, model lifecycle, calibration 책임 |

### Jev의 confidence

Jev에서 `Choice`와 `Score`의 `confidence`는 option/level probability distribution의 집중도를 0–1로 요약한다. `Noul`에는 같은 `confidence` field가 없으므로 반환 확률과 별도 정책을 사용한다.

> [!NOTE]
> threshold는 모델의 보증이 아니다. action의 위험도와 실제 domain data의 error cost에 따라 달라진다.

### laya checkpoints

| Checkpoint | 기반 | 규모 | 기본 context | 용도 |
|---|---:|---:|---:|---|
| `laya` | ModernBERT-large | 421M | 512 | English |
| `laya-multilingual` | mmBERT-base | 322M | 1024 | multilingual |
| `laya-typed-decisions` | ModernBERT-large | 421M | 512 | typed-decision workflow |

repository는 `laya-multilingual`이 `max_len=8192`로 encoder의 긴 context를 사용할 수 있다고 안내한다. 긴 문서·negation·다수 option은 별도 평가 대상이다.

## Sources

- https://docs.typesafe.ai/introduction
- https://docs.typesafe.ai/confidence
- https://github.com/NandhaKishorM/laya
- https://huggingface.co/convaiinnovations/laya
