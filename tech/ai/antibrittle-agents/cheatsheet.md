---
date: 2026-06-24
tags:
  - tech
  - ai
  - agents
  - cheatsheet
  - reliability
type: tech-tool-study
parent: "[[README]]"
---

# Antibrittle Agents - 치트시트

> [[05-projects|이전: 프로젝트]] | [[README|목차로 돌아가기]]

---

## 핵심 정의

```text
Antibrittle Agents
= long-horizon agent가 실패·분기·재시도·불확실성을
  observable runtime structure로 흡수하게 만드는 architecture pattern
```

---

## 키워드

| Term | 한국어 설명 | 핵심 질문 |
|------|-------------|-----------|
| Agentic loop | goal+tool+LLM 반복 실행 | loop가 진전되고 있는가? |
| Task horizon | 작업이 이어지는 시간/step 길이 | 몇백 loop 후에도 안정적인가? |
| Run box | 행동 범위 metric | 좋은/나쁜 trajectory signal은 무엇인가? |
| Region of freedom | 탐색 허용 영역 | 어디까지 agent가 자유롭게 탐색해도 되는가? |
| Trench | context boundary | 다음 step에 필요한 artifact가 명확한가? |
| Receipt | 추적 가능한 근거 | 결론을 source/tool/script로 역추적 가능한가? |
| Tool minimalism | tool surface 최소화 | tool이 capability보다 noise를 늘리고 있지는 않은가? |
| Human interruption point | 사람 개입 지점 | 언제 사람이 봐야 가장 효과적인가? |

---

## 설계 체크리스트

### Before building

- [ ] 이 작업은 agentic loop가 필요한 긴 horizon 작업인가?
- [ ] deterministic script나 batch job으로 충분하지 않은가?
- [ ] subproblem graph가 정의되어 있는가?
- [ ] 각 subproblem의 handoff artifact가 있는가?

### Runtime

- [ ] loop trace를 남기는가?
- [ ] retry/backoff/recovery policy가 있는가?
- [ ] irreversible action 전 human approval이 있는가?
- [ ] checkpoint 또는 rollback point가 있는가?

### Run boxes

- [ ] source diversity를 측정하는가?
- [ ] repeated failed tool calls를 감지하는가?
- [ ] loop stagnation을 감지하는가?
- [ ] cost/latency variance를 추적하는가?
- [ ] receipt coverage를 계산하는가?

### Receipts

- [ ] final claim마다 source/tool/script/decision이 연결되는가?
- [ ] source timestamp 또는 retrieval metadata가 있는가?
- [ ] script output checksum이나 command log가 있는가?
- [ ] 사람이 audit할 수 있는 artifact가 남는가?

### Tool surface

- [ ] 핵심 tool 3~5개로 시작했는가?
- [ ] tool description이 명확하고 짧은가?
- [ ] tool permission이 least privilege인가?
- [ ] 사용하지 않는 MCP/tool을 제거했는가?

---

## 빠른 Metric 예시

| Metric | Formula / Rule |
|--------|----------------|
| Receipt coverage | `claims_with_receipt / total_key_claims` |
| Tool failure repeat | same `tool_name + args_hash` error count |
| Stagnation | loops without new artifact |
| Source diversity | unique source domains |
| Trajectory variance | stddev of loop count/tool path across repeated runs |
| Cost variance | stddev of token/cost/latency across repeated runs |

```yaml
quality_gate:
  receipt_coverage: ">= 0.9"
  repeated_tool_failure: "<= 2"
  stagnation_loops: "<= 3"
  source_diversity: ">= 3"
  human_approval:
    - irreversible_action
    - production_write
```

---

## 구현 매핑

| Antibrittle 개념 | 구현 후보 |
|------------------|-----------|
| Agentic loop | OpenAI Agents SDK, LangGraph, CrewAI |
| Trenches | graph node, workflow step, class/service boundary |
| Receipts | trace store, artifact directory, provenance DB |
| Tool minimalism | core shell/read/edit/fetch tools, curated MCP server |
| Human interruption | approval node, guardrail, queue, UI review |
| Perturbation test | eval harness, CI scenario tests |

---

## Anti-patterns

| Anti-pattern | 문제 |
|--------------|------|
| "tool을 많이 붙이면 똑똑해진다" | context pollution과 wrong tool call 증가 |
| "TODO list면 충분하다" | 비선형 dependency와 state boundary가 사라짐 |
| "subagent를 많이 만들면 빨라진다" | sibling communication cost 폭증 |
| "trace dashboard만 붙이면 된다" | recovery strategy와 boundary가 없으면 관찰만 가능 |
| "final answer만 평가한다" | trajectory failure와 brittle behavior를 놓침 |

---

## 최소 Template

```markdown
## Task
- Goal:
- Horizon:
- Risk:

## Subproblem Graph
- Node:
- Input:
- Output:
- Exit criteria:

## Run Box
- Good signals:
- Bad signals:
- Interrupt triggers:

## Receipts
- Source/tool/script:
- Claim mapping:
- Audit path:
```

---

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp/cheatsheet]] - MCP tool/resource quick reference
- [[study/tech/ai/lazy-codex/cheatsheet]] - verification harness quick reference
- [[study/tech/ai/agent-orchestration/README]] - orchestration reference
