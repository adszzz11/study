---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev Deep Dive

> [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. Atomic decision design

“이 agent가 다음에 무엇을 해야 하는가?”처럼 복합 질문 하나를 던지지 않는다. 아래처럼 분리한다.

```text
task_type?       → Choice: search | summarize | execute | other
contains_pii?    → Noul
needs_approval?  → Noul
impact?          → Score: low | medium | high
```

그 후 weight, action precedence, access check는 version-controlled application code가 결정한다. 이렇게 하면 audit, policy 변경, failure analysis가 쉬워진다.

## 2. Confidence와 3단계 policy

| 조건 | 처리 | 예 |
|---|---|---|
| high confidence + low impact | auto-act | safe queue assignment |
| medium confidence 또는 medium impact | confirm / review | operator confirmation |
| low confidence 또는 high impact | stop / fallback | human approval, rule engine, stronger model |

Choice/Score의 confidence는 uncertainty signal이지 correctness 보증이 아니다. Noul은 probability를 risk threshold와 결합하고, destructive action에서는 approval을 별도 gate로 둔다.

## 3. Calibration evaluation

1. historical log에서 label과 outcome이 있는 sample을 분리한다.
2. Jev result, model version, question schema, confidence/probability, latency를 저장한다.
3. confidence bucket별 accuracy와 coverage를 계산한다.
4. threshold별 auto-act error, review rate, latency, business cost를 비교한다.
5. 시간·언어·customer segment별 drift와 `other` 비율을 모니터링한다.

```text
coverage = auto-acted cases / all cases
error_rate = incorrect auto-actions / auto-acted cases
```

vendor evaluation은 출발점일 뿐이고, threshold는 자신의 risk appetite와 domain label을 기준으로 정한다.

## 4. 안전한 실행 boundary

- Jev output을 tool name, URL, permission, money movement로 직접 변환하지 않는다.
- action allowlist와 caller authorization을 code에서 재검증한다.
- write operation은 idempotency key, audit log, retry semantics를 둔다.
- API failure·timeout·malformed integration result에는 fail closed 또는 safe fallback을 정한다.
- model alias를 쓸 때와 version pin을 쓸 때의 rollout·rollback 절차를 구분한다.

## Sources

- https://docs.typesafe.ai/primitives
- https://docs.typesafe.ai/confidence
- https://typesafe.ai/blog/introducing-system-one-models-and-jev
