---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Harness² project ideas

## 1. Coding agent harness improvement

반복되는 code review, migration, test-fix workflow를 대상으로 `AGENTS.md`, skill/tool guidance, subagent topology를 candidate surface로 둔다. CI와 human review는 Harness²와 별개인 adoption gate로 유지한다.

## 2. Internal specialist agent

법무·조달·지원 domain마다 lesson library를 쌓는다. reflection artifact로 PII나 비밀정보가 흘러가지 않도록 redaction을 먼저 넣고, domain expert가 샘플을 승인한다.

## 3. Agent regression lab

배포 후보 harness와 기준 harness를 쌍으로 실행한다. `--bases` 평가, sealed eval set, 비용·latency·안전성 지표를 함께 보고해 성능만 좋아진 후보의 promotion을 막는다.

## 4. Multi-model portability study

동일 harness를 여러 executor/model에 적용한다. 모델 교체에도 남는 harness invariant와 특정 모델에만 맞는 prompt/tool guidance를 분리해 기록한다.

## Recommended delivery flow

```text
isolated improvement workspace
  → candidate patch + evidence
  → eval and security review
  → human approval
  → controlled promotion
```

production agent가 바로 self-modify하도록 두는 것보다, 이 분리 구조가 rollback·audit·access control에 유리하다.
