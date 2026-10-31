---
date: 2026-06-24
tags:
  - tech
  - ai
  - agents
  - deep-dive
  - reliability
type: tech-tool-study
parent: "[[../README]]"
---

# Antibrittle Agents - 심화

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 목표

기본 trace를 넘어 **trenches**, **regions of freedom**, **perturbation testing**, **tool minimalism**, **human interruption points**를 설계한다.

---

## 1. Trenches 설계

Trench는 context rot를 막기 위한 boundary다. 핵심은 "다음 step이 이전 step의 전체 transcript를 읽지 않아도 일할 수 있는가?"다.

| Boundary | Handoff artifact | 통과 조건 |
|----------|------------------|-----------|
| Research planning | query set, inclusion/exclusion criteria | source selection 가능 |
| Evidence extraction | claim/evidence table | synthesis 가능 |
| Code localization | suspected files, rationale | patch planning 가능 |
| Patch execution | diff, test result, rollback point | review 가능 |

```yaml
trench:
  name: evidence_extraction
  input:
    - selected_sources.json
  output:
    - evidence_table.md
    - receipts/
  exit_criteria:
    - every key claim has source_url
    - conflicting evidence is marked
    - low-confidence claims are excluded
```

---

## 2. Regions of freedom

Agent에게 완전한 자유를 주거나 모든 step을 고정하지 않는다. 탐색이 필요한 영역과 통제가 필요한 영역을 분리한다.

| 영역 | Agent 자유도 | Control |
|------|--------------|---------|
| Query expansion | 높음 | domain blacklist, max queries |
| Source selection | 중간 | source quality criteria |
| Irreversible action | 낮음 | human approval |
| Final claim writing | 중간 | receipt coverage gate |

```text
Exploration region:
  "Find 10 candidate sources within budget"

Choke point:
  "Select 5 sources, justify inclusion/exclusion"

Execution region:
  "Extract claims only from selected sources"
```

---

## 3. Perturbation test

같은 task를 여러 변형으로 실행해 consistency와 robustness를 본다.

| Perturbation | 목적 | 관찰할 것 |
|--------------|------|-----------|
| Paraphrase task | 표현 변경 내성 | 동일한 subproblem graph가 나오는가 |
| Tool timeout | tool failure 회복 | retry/backoff/alternative path |
| Reordered JSON | schema robustness | field order에 흔들리는가 |
| Missing field | partial data 처리 | graceful degradation |
| Stale source | freshness 판단 | 오래된 source를 표시/배제하는가 |

```bash
# conceptual
agent-harness run task.yaml --variant paraphrase --repeat 5
agent-harness run task.yaml --variant tool-timeout --repeat 5
agent-harness report runs/* --metrics consistency,trajectory_variance,cost_variance
```

---

## 4. Tool minimalism 실험

Tool이 많으면 capability는 늘지만 context pollution과 action ambiguity도 늘어난다.

| 실험군 | Tool set | 측정 |
|--------|----------|------|
| Minimal | Read, Write/Edit, Shell, Fetch | latency, failure mode, receipt coverage |
| Expanded | 20개 MCP/tool | wrong tool call, context size, repeated failure |

평가 질문:

- 같은 task success에서 minimal set이 더 예측 가능한가?
- tool description이 context를 얼마나 차지하는가?
- 실패 시 recovery path가 명확한가?
- tool permission이 least privilege인가?

---

## 5. Human interruption points

사람이 모든 token을 볼 수 없으므로 개입 지점을 signal 기반으로 설계한다.

| Trigger | 예시 | Human action |
|---------|------|--------------|
| Risk | production write, payment, delete | approve/reject |
| Cost anomaly | budget 2배 초과 | continue/stop |
| Low confidence | evidence conflict, receipt missing | request more evidence |
| Loop stagnation | 3회 이상 progress 없음 | re-plan |
| Boundary exit | major trench 완료 | review artifact |

```yaml
interruptions:
  - trigger: irreversible_action
    require: human_approval
  - trigger: receipt_coverage_below_0_9
    require: evidence_review
  - trigger: stagnation_loop_gt_3
    require: replan
```

---

## 6. Single-thread vs Multi-agent

Southbridge 관점에서는 무조건적인 multi-agent fanout이 답이 아니다. 병렬화는 독립적인 map-like 작업에서 효과적이고, shared state가 많은 문제에서는 communication cost가 커진다.

| 문제 유형 | 추천 |
|-----------|------|
| 독립 source 100개 요약 | parallel map 가능 |
| 하나의 복잡한 architecture decision | single-thread 우선 |
| codebase 전체 grep + 후보 파일 scoring | 병렬 가능 |
| patch 설계와 적용 | boundary가 명확할 때만 분리 |

```text
Good parallelism:
  source_i -> extraction_i -> merge

Bad parallelism:
  agent_a guesses state
  agent_b guesses state
  agent_c reconciles conflicting guesses
```

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/cli-agents]] - orchestration과 subagent tradeoff
- [[study/tech/ai/multi-agent-platforms]] - multi-agent framework 비교
- [[study/tech/ai/model-context-protocol-mcp]] - tool surface와 permission boundary
