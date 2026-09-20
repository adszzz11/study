---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Prime Agent — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## Project Ladder

모든 프로젝트는 disposable clone/container, least privilege, external verifier를 기본 조건으로 한다.

| 단계 | 프로젝트 | 학습 목표 | 위험도 |
|---|---|---|---|
| 1 | Context-efficient log analyst | L2 filtering과 selective print | 낮음 |
| 2 | Durable repository cartographer | detach/reattach와 checkpoint | 낮음 |
| 3 | Recursive code review team | child contract, messaging, accounting | 중간 |
| 4 | Continual Harness canary lab | refinement diff, provenance, rollback | 높음 |
| 5 | Provider-neutral harness benchmark | model/provider/harness 조건 통제 | 중간 |

## 1. Context-Efficient Log Analyst

### Goal

대형 build/test log를 REPL에서 처리하고 active context에는 실패 cluster와 대표 evidence만 넣는다.

### Build

- log parser와 normalization function 작성
- error signature별 aggregation
- top cluster와 대표 line만 `print()`
- 전체 log 출력 방식과 token/cost 비교

### Acceptance Criteria

- [ ] 모든 known error fixture를 탐지한다.
- [ ] summary에서 source line으로 역추적할 수 있다.
- [ ] active context에 전체 log가 들어가지 않는다.
- [ ] parser 결과를 immutable fixture test가 독립 검증한다.

## 2. Durable Repository Cartographer

### Goal

큰 repository의 module, entry point, test coverage map을 여러 session에 걸쳐 만든다.

### Workflow

```text
set durable goal
  -> scan paths into L2
  -> checkpoint normalized facts into L3
  -> detach
  -> heartbeat/reattach
  -> invalidate stale facts
  -> render final map
```

### Acceptance Criteria

- [ ] client 종료 후에도 objective와 history가 복구된다.
- [ ] generated map의 모든 node가 실제 file/symbol evidence를 가진다.
- [ ] deleted/renamed file이 다음 run에서 invalidated 된다.
- [ ] secret file과 excluded path를 읽지 않는다.

## 3. Recursive Code Review Team

### Roles

| Child | Scope | Deliverable |
|---|---|---|
| `auth-reviewer` | authentication code | concrete risk + path/symbol evidence |
| `test-reviewer` | relevant tests | missing invariant + proposed test |
| `dependency-reviewer` | lockfile and manifests | risky dependency/use site |

Root는 세 결과를 합치고 contradiction과 duplicate를 제거한다. 첫 실습에서는 모두 read-only로 제한한다.

### Budget

```yaml
max_depth: 1
max_concurrency: 3
max_wall_time_minutes: 20
max_turns_per_child: 12
network: deny
writes: deny
```

위 YAML은 design example이며 실제 configuration schema가 아니다. 현재 공식 문서의 budget option에 맞춰 옮긴다.

### Acceptance Criteria

- [ ] child마다 stable handle과 독립 artifact가 있다.
- [ ] root accounting에 모든 descendant가 포함된다.
- [ ] finding은 file/symbol evidence 없이 채택되지 않는다.
- [ ] external static analysis/test 결과와 교차 검증한다.

## 4. Continual Harness Canary Lab

### Goal

반복되는 작은 task에서 `/refine`이 prompt note, memory, skill, subagent specification 중 무엇을 바꾸는지 관찰한다.

### Guardrails

- refinement state를 별도 version control에 저장
- candidate diff를 human review 전 적용하지 않음
- canary task와 immutable hidden test 분리
- network/credential scope 확대 금지
- exploit, test deletion, verifier 수정 시 즉시 rollback

### Experiment Matrix

| Run | Harness version | Refinement | Canary score | Hidden score | Security diff | Decision |
|---|---|---|---:|---:|---|---|
| A | baseline | none |  |  | none |  |
| B | candidate-1 | prompt note |  |  |  |  |
| C | candidate-2 | skill |  |  |  |  |

### Acceptance Criteria

- [ ] 모든 state 변경에 source trajectory와 provenance가 있다.
- [ ] hidden verifier는 agent가 수정할 수 없다.
- [ ] score 상승이 shortcut/reward hacking이 아님을 검토한다.
- [ ] rollback 후 baseline behavior를 재현한다.

## 5. Provider-Neutral Harness Benchmark

### Goal

동일한 작은 coding/research suite에서 provider와 harness condition을 통제해 비교한다.

### Record

```yaml
date: 2026-09-01
prime_agent_commit: <sha>
model_snapshot: <exact-id>
provider: <provider>
context_limit: <tokens>
budget: <cost/time/turn>
child_concurrency: <n>
refinement_state: <version-or-none>
evaluator_commit: <sha>
runs: <n>
```

### Acceptance Criteria

- [ ] model snapshot과 provider를 별도로 기록한다.
- [ ] 동일 evaluator·budget·environment를 사용한다.
- [ ] mean뿐 아니라 run별 결과와 failure를 공개한다.
- [ ] Best@k는 총 비용과 함께 보고한다.
- [ ] developer claim과 local reproduction을 구분한다.

## Project Retrospective

각 프로젝트 뒤 다음을 기록한다.

- L1에 불필요하게 유입된 data는 무엇인가?
- L2/L3의 stale state가 판단을 왜곡했는가?
- delegation이 실제 wall time과 quality를 개선했는가?
- external verifier가 agent의 잘못된 확신을 잡았는가?
- refinement가 실제 procedure를 개선했는가, reward를 exploit했는가?
- root와 descendant의 전체 cost가 허용 범위였는가?

## Sources

- [공식 Quickstart](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/quickstart.md)
- [Architecture documentation index](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/index.md)
- [Refine skill](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/skills/refine/SKILL.md)
- [Prime Agent 기술 논문](https://arxiv.org/html/2608.23552)

