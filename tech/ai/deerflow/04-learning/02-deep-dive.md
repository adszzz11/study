---
date: 2026-10-11
tags: [tech]
type: tech-tool-study
status: draft
---

# DeerFlow — 심화

> [[../README|목차로 돌아가기]] | [[01-getting-started|이전: 시작하기]]

## 1. Delegation 설계

subagent는 main thread를 길게 만드는 수단이 아니라, 독립 context에서 검증 가능한 하위 결과를 만드는 boundary다.

```text
Lead Agent
 ├─ general-purpose: 경쟁사 문서 조사
 ├─ general-purpose: release note 변화 추출
 └─ bash: 허용된 workspace에서 표·chart artifact 생성
                 ↓
          Lead Agent가 source·artifact를 종합
```

각 task에는 목표, 허용 source/tool, 기대 산출물, 완료 기준을 넣는다. subagent output은 신뢰된 사실이 아니라 검토 대상 evidence로 취급한다.

## 2. Middleware와 Config

middleware chain은 모델 호출의 전후에 summarization, memory, guardrail, tool policy를 결합한다. 변경은 한 번에 여러 개를 하지 말고 다음처럼 실험한다.

1. 기준 config와 task set을 고정한다.
2. middleware 또는 tool group 하나만 바꾼다.
3. task success, citation fidelity, tool error rate, cost, latency를 비교한다.
4. 결과가 나쁘면 config를 되돌리고 로그에서 failure mode를 분류한다.

## 3. Memory와 Durable State

checkpoint는 실행 재개에, memory는 이후 turn에 필요한 정보를 선택적으로 제공하는 데 쓰인다. 둘을 같은 것으로 취급하지 않는다.

| 구분 | 질문 | 점검 |
|---|---|---|
| checkpoint | 중단된 graph를 재개할 수 있는가? | DB backup, schema migration, recovery test |
| application data | 프로젝트·대화가 올바르게 분리되는가? | tenant/project authorization |
| memory | 오래된 요약이 잘못된 결론을 강화하지 않는가? | expiry, source link, correction path |

## 4. Production Boundary

v2.1 계열의 durable batch delegation, pluggable memory backend, extension system, auth/authz, project·conversation branching은 기능 도입 자체보다 운영 경계를 검증해야 한다는 신호다.

- multi-user 환경에서는 LocalSandbox 대신 격리된 provider를 선택한다.
- custom agent마다 skill·tool group을 whitelist하고 credential을 분리한다.
- 외부 write, deploy, 결제, production command는 human approval 뒤에 실행한다.
- untrusted web page/PDF의 instruction은 data로 취급하고 prompt injection을 검사한다.
- checkpoint DB, artifact storage, audit log의 보존·backup·삭제 정책을 문서화한다.

## Evaluation Matrix

| 축 | 측정 예 |
|---|---|
| 품질 | task success, citation fidelity, artifact correctness |
| 안정성 | retry 성공률, resume 성공률, tool error rate |
| 보안 | denied action 동작, sandbox escape test, secret leak 여부 |
| 운영 | p95 latency, token/tool cost, trace와 audit completeness |

## Sources

- https://deerflow.tech/en/docs/harness/design-principles
- https://deerflow.tech/en/docs/harness/subagents
- https://deerflow.tech/en/docs/tutorials/work-with-memory
- https://github.com/bytedance/deer-flow/releases

## 추가 조사: Durable Fan-out과 Batch Orchestration

오케스트레이션에서 병렬 실행(parallelism)은 "가능하면 많이"가 아니라, **대화형 위임과 대량 작업을 서로 다른 실행 계약(execution contract)으로 분리**하는 문제다. DeerFlow 2.1의 일반 `task`는 Lead Agent가 결과를 기다린 뒤 종합하는 대화형 위임에, opt-in `batch_task`는 SQL persistence와 lease·retry·pause/resume/cancel을 갖는 대량 독립 항목 처리에 맞는다.

| 구분 | `task` / synchronous delegation | `batch_task` / durable batch |
|---|---|---|
| 적합한 입력 | 결과가 다음 reasoning에 바로 필요한 소수의 subtask | 서로 독립적인 다수 항목(문서·URL·레코드) |
| Lead Agent의 동작 | 결과를 받은 뒤 evidence를 비교·종합 | batch receipt를 받고 progress/result를 별도 조회 |
| 상태 보존 | run 범위의 delegation ledger와 subagent history | SQL-backed item 상태, lease, retry, pause/resume/cancel |
| 핵심 위험 | 과도한 fan-out, context에 결과를 모두 주입 | item 중복 제출, lease 만료, 무한 재시도, 결과 폭주 |
| 운영 제어 | `max_concurrent_subagents`, `max_total_subagents`, token/turn/timeout budget | batch item 수·live/running capacity·lease·retry·retention |

실무적으로는 다음의 **two-plane pattern**이 유용하다.

```text
Control plane: Lead Agent
  ├─ batch 정의·예산·concurrency·취소/승인 정책
  ├─ batch receipt / aggregate progress 확인
  └─ 표본 결과와 aggregate만 context로 받아 최종 판단

Data plane: durable workers
  └─ item claim → sandbox 실행 → bounded result/evidence 저장 → retry 또는 terminal state
```

- `task`에는 서로 다른 질문과 명확한 완료 조건을 준다. 단순히 "더 찾아봐"를 여러 번 보내면 redundant re-delegation과 synthesis 비용만 증가한다.
- batch 항목은 입력 snapshot, 항목 식별자, 허용 tool/source, 최대 시도 횟수, terminal failure 처리 규칙을 함께 보존한다. 재개(resume) 가능한 작업은 **재실행해도 안전한 idempotent write** 또는 별도 commit 단계가 필요하다.
- worker 결과 전체를 model context에 넣지 않는다. 집계 지표, 실패 표본, 사용자가 요청한 결과만 가져오고 원본은 artifact/DB에 둔다.
- concurrency는 모델 rate limit뿐 아니라 sandbox slot, search provider quota, DB connection, 사람의 review 처리량까지 포함해 정한다. 독립 subagent 수와 실제 안전한 동시 실행 수는 다르다.

## 추가 조사: Verifiable Delegation과 Evidence Contract

좋은 위임은 "subagent가 그럴듯한 보고를 반환했다"가 아니라 **무엇을 실행했고 무엇이 검증되었는지 Lead Agent가 판정할 수 있는 계약**을 만든다. DeerFlow 2.1 release는 tool receipt, subagent report의 deliverable handle, parent-side deterministic acceptance check를 이 방향의 runtime 기능으로 제시한다. 판정 불가능한 항목은 성공으로 추정하지 않고 `UNVERIFIED`로 남기는 것이 핵심이다.

| 산출물 종류 | acceptance criteria 예 | 자동 판정 가능 여부 |
|---|---|---|
| 파일·chart artifact | 지정 경로 존재, non-empty, checksum/형식 확인 | 가능 |
| 코드 변경 | 허용된 test command의 exit status와 로그 | 가능(테스트 범위 내) |
| 조사 report | URL·수집 시각·claim ID 존재 | 일부 가능 |
| "결론이 타당함" | source fidelity, 비교의 공정성, 누락 여부 | 사람 또는 별도 평가 필요 |

```yaml
# 의사 코드(pseudocode): delegation의 최소 evidence contract
delegation:
  objective: "공식 문서 20건에서 breaking change를 추출"
  allowed_sources: ["docs.example.com", "github.com/org/project"]
  allowed_tools: [web_search, web_fetch, write_file]
  deliverables:
    - path: "artifacts/release-diff.md"
      checks: [exists, non_empty]
  acceptance_criteria:
    - "각 claim에 원문 URL과 수집 시각이 있다"
    - "허용되지 않은 외부 write가 없다"
  on_undecidable: "UNVERIFIED"
```

- receipt/trace ID는 **감사와 상관관계(correlation)** 용도이지 사실성의 증명이 아니다. URL이 있어도 원문이 claim을 지지하는지 표본 검토한다.
- Lead Agent는 raw prose보다 `claim → source → tool receipt → deliverable` 링크를 요구하고, synthesis 단계에서 서로 충돌하는 claim을 명시한다.
- delegation ledger에는 dispatch 시점의 prompt/context snapshot, 모델·skill·tool version, budget 소진/timeout 사유를 남긴다. 그래야 재현(reproducibility)과 cost attribution이 가능하다.

## 추가 조사: Human-in-the-loop Interrupt와 Research Control Loop

긴 research orchestration은 한 번의 run이 아니라 **관찰(observe) → 판단(decide) → 승인(approve) → 실행(act) → 재개(resume)** 루프다. DeerFlow의 기반인 LangGraph에서는 durable checkpointer가 thread 상태를 저장하고 `interrupt()`가 외부 입력까지 실행을 멈췄다가 `Command`로 재개하는 형태를 제공한다. 이를 이용해 승인 지점을 prompt 관습이 아닌 상태 전이(state transition)로 둔다.

```text
Plan → Dispatch read-only research → Evaluate evidence
                                  ↓
                    [interrupt: side effect approval]
                                  ↓
                      scoped action → receipt/audit → next checkpoint
```

승인은 다음 정보를 묶어야 한다: 대상(target), 작업(action), 영향 범위(scope), 근거(evidence), 만료 시간(expiry), 재개할 run/checkpoint ID. "진행해"라는 대화 문장만으로 write·deploy·외부 전송을 재개시키면 stale approval과 prompt injection을 구분하기 어렵다.

연구용 최소 scorecard는 quality뿐 아니라 orchestration 자체를 측정한다.

| 질문 | 관측 지표(metric) |
|---|---|
| fan-out이 실제로 효과적인가? | wall-clock 감소 대비 token/tool cost, 중복 delegation 비율 |
| 재개가 안전한가? | checkpoint restore 성공률, retry 후 duplicate side effect 수 |
| human gate가 작동하는가? | 승인 전 차단률, expired approval 거부율, override audit completeness |
| evidence가 신뢰할 만한가? | citation fidelity 표본 점수, `UNVERIFIED` 비율, conflict 해결률 |

## 추가 조사 Sources

- https://github.com/bytedance/deer-flow/releases/tag/v2.1.0
- https://deerflow.tech/en/docs/harness/subagents
- https://deerflow.tech/en/docs/harness/configuration
- https://langchain-ai.github.io/langgraph/concepts/durable_execution/
- https://langchain-ai.github.io/langgraph/concepts/breakpoints/
