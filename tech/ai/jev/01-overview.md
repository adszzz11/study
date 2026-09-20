---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Jev는 TypeSafe AI의 System One decision API다. `state`(text 또는 JSON)와 `questions`를 보내면 각 질문을 같은 state에 대해 독립적으로 병렬 평가해 typed result를 반환한다. 모델이 허용되지 않은 action을 문장으로 발명하지 않도록 application이 question과 option/rubric을 정한다.

## Why

Generative LLM은 사람에게 읽힐 문장 생성에 강하다. 그러나 software decision에는 보통 JSON 생성, parse, schema validation, retry, error handling이 추가된다. Jev는 typed probability를 반환해 그 변환 계층을 줄이고, 결정과 실행을 분리한다.

## Primitives

| Primitive | 입력 의도 | 결과 | 적합한 질문 |
|---|---|---|---|
| `Choice` | 비순서형 option 집합 | 선택값, 전체 `probabilities`, `confidence` | “어느 부서가 담당인가?” |
| `Score` | 순서형 level/rubric | score, 분포, `confidence` | “frustration은 어느 수준인가?” |
| `Noul` | 명확한 yes/no 명제 | `0..1` probability | “이 ticket은 urgent인가?” |

`confidence`는 Choice/Score의 probability distribution에서 계산된다. Noul에는 별도 confidence가 없으므로 probability와 action risk를 함께 policy에 반영한다.

## 설계 원칙

1. 복합 판단 대신 atomic question으로 분해한다.
2. Choice에는 `other` 또는 `none`을 넣어 closed-world assumption의 탈출구를 만든다.
3. model output은 decision signal일 뿐이다. allowlist, authorization, idempotency, human approval은 일반 code에서 다시 확인한다.
4. destructive action일수록 auto-act confidence threshold를 높이고 low confidence는 review/fallback으로 보낸다.

> [!WARNING]
> Jev는 early access 제품이다. vendor benchmark나 공개 latency 수치를 production SLO로 가정하지 말고, 실제 traffic과 labeled outcome으로 정확도·calibration을 검증한다.

## Hybrid architecture

```text
Request ─► Jev: risk / task type / route
               ├─ rule engine
               ├─ cheap LLM
               ├─ strong LLM
               └─ human review
                    │
               application authorization
```

Jev는 LLM의 대체재보다 decision layer에 가깝다. 생성과 깊은 reasoning은 선택된 LLM이, 실행 안전성은 business rule과 authorization layer가 맡는다.

## Sources

- https://docs.typesafe.ai/introduction
- https://docs.typesafe.ai/primitives
- https://docs.typesafe.ai/confidence
