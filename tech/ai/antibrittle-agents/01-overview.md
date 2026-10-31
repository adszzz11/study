---
date: 2026-06-24
tags:
  - tech
  - ai
  - agents
  - reliability
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# Antibrittle Agents - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - Antibrittle Agents란?

Antibrittle Agents는 특정 라이브러리명이라기보다 **long-horizon AI agent를 덜 brittle하게 만드는 architecture pattern**이다. LLM agent가 긴 작업 중 실패하지 않기를 기대하는 대신, 실패·분기·재시도·불확실성을 runtime 안에서 관찰하고 회복 가능한 구조로 흡수한다.

| 관점 | 설명 |
|------|------|
| Primitive | 단일 `LLM call`이 아니라 `agentic loop` |
| 목표 | stochastic failure 제거가 아니라 장시간 생산성 유지 |
| 설계 대상 | runtime, boundary, observability, accountability |
| 핵심 질문 | "정답인가?"뿐 아니라 "좋은 trajectory로 가고 있는가?" |

```text
Agent = LLM in a loop with tools and a goal

Long task success
  = model quality
  + loop control
  + context discipline
  + tool discipline
  + traceability
  + recovery points
```

---

## 2. Why - 왜 필요한가?

### 문제 배경

짧은 demo에서는 agent가 똑똑해 보이지만, 실제 업무는 긴 task horizon을 가진다. research, code maintenance, reconciliation, data mining처럼 수십~수천 step이 필요한 작업에서는 단일 응답 품질보다 **loop가 얼마나 오래 안정적으로 유지되는지**가 중요하다.

긴 작업에서 흔한 failure mode는 다음과 같다.

| Failure mode | 설명 | 결과 |
|--------------|------|------|
| Context rot | 오래된 context가 누적되어 판단 품질이 떨어짐 | 잘못된 전제, 반복 실수 |
| Tool explosion | 너무 많은 tool이 context와 decision space를 오염 | latency 증가, 잘못된 tool call |
| Fake linear TODO | 비선형 문제를 TODO list로 억지 선형화 | subproblem 간 의존성 붕괴 |
| Sibling communication cost | subagent fanout 후 상호 설명 비용 폭증 | 병렬화 이득 상실 |
| Missing rationale | 판단 근거와 source가 남지 않음 | audit, rollback, review 불가 |

2025-2026년 agent reliability 논의도 평균 task success만으로 실제 reliability를 설명하기 어렵다고 본다. consistency, robustness, predictability, safety, accountability를 따로 측정해야 한다.

### 핵심 전환

```text
Before:
  Better model -> better answer

After:
  Better runtime + boundaries + receipts -> longer useful work
```

Antibrittle 관점에서는 "모델을 완벽하게 만들자"보다 "실패해도 어디서, 왜, 어떻게 실패했는지 알고 회복 가능한 구조를 만들자"가 우선이다.

---

## 3. 핵심 특징

### Run boxes

Run box는 개별 LLM call의 성공/실패가 아니라 agentic loop의 행동 범위를 관찰하는 개념이다. research agent라면 최종 답변만 보지 않고 fetch 수, source diversity, link-follow depth, repeated failed tool calls 같은 행동 signal을 본다.

| Metric 예시 | 좋은 signal | 나쁜 signal |
|-------------|-------------|-------------|
| Source diversity | 독립 domain/source 증가 | 한 source만 반복 |
| Link-follow depth | 근거까지 추적 | 얕은 snippet만 사용 |
| Loop progress | subproblem artifact 증가 | 같은 tool failure 반복 |
| Cost variance | 예측 가능한 비용 | runaway loop |
| State size | boundary별 state 유지 | 무제한 context accumulation |

### Regions of freedom

모든 step을 강제하지 않는다. 대신 subproblem별로 agent가 탐색할 수 있는 영역과 반드시 통과해야 하는 choke point를 나눈다. 즉 exploration-exploitation을 prompt가 아니라 runtime 설계 문제로 본다.

```text
Open exploration region
  -> candidate evidence / solution paths
  -> choke point review
  -> constrained execution region
```

### Trenches

Trench는 subproblem 사이에 만드는 단단한 context boundary다. service/class/workflow step처럼 state handoff를 명확히 하여 context rot와 task avalanche를 줄인다.

| Trench 대상 | Boundary artifact |
|-------------|-------------------|
| Research query generation | query set, source criteria |
| Evidence synthesis | citation map, claim table |
| Code patching | diff, test plan, rollback point |
| Data reconciliation | discrepancy table, reproducible script |

### Receipts

Southbridge의 표현을 빌리면 목표는 "five nines reliability" 이전에 **five nines accountability**다. 최종 결론이 어떤 source, tool result, script, intermediate decision에서 나왔는지 추적 가능해야 한다.

### Tool minimalism

MCP/tool을 많이 붙이는 것이 항상 좋지 않다. context window를 오염시키는 20개 tool보다 `Read`, `MultiEdit`, `Shell`처럼 단순하고 강한 tool set이 긴 작업에서 더 안정적일 수 있다.

### Human interruption points

긴 horizon에서는 사람이 모든 intermediate token을 볼 수 없다. 따라서 개입 시점은 "매 step 승인"이 아니라 run box signal, risk score, cost anomaly, irreversible action 직전처럼 설계해야 한다.

### Single-thread 우선

무작정 multi-agent fanout을 늘리면 sibling communication cost가 커진다. 병렬화는 독립적인 map-like 문제에 선별 적용하고, stateful reasoning은 single-thread를 우선한다.

---

## 4. 장점과 한계

| 구분 | 내용 |
|------|------|
| 장점 | 긴 작업에서 failure visibility, rollback, audit, recovery 가능성이 커진다. |
| 장점 | agent 설계를 prompt가 아니라 runtime/control/observability 문제로 다룬다. |
| 한계 | framework만 설치한다고 자동으로 생기지 않는다. metric, boundary, receipt schema를 직접 설계해야 한다. |
| 한계 | 모든 작업을 agentic loop로 만들면 overhead가 커진다. 짧고 결정적인 작업은 conventional script가 낫다. |

---

## 관련 노트

- [[study/tech/ai/lazy-codex]] - verified completion과 false completion 방어
- [[study/tech/ai/model-context-protocol-mcp]] - tool minimalism과 tool/data protocol 관점
- [[study/tech/ai/agent-orchestration/cli-agents]] - agent orchestration과 single-thread/multi-agent tradeoff

## References

- [Southbridge.AI - Antibrittle Agents](https://www.southbridge.ai/blog/antibrittle-agents)
- [Rabanser et al. - Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666)
- [Sinha et al. - The Illusion of Diminishing Returns](https://arxiv.org/abs/2509.09677)
