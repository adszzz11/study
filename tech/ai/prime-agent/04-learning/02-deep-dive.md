---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Prime Agent — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차]] · [[../05-projects|다음: Projects]]

## 1. Designing Across L0–L3

좋은 Prime Agent workflow는 정보를 계층별로 의도적으로 배치한다.

| 질문 | 권장 계층 | 이유 |
|---|---|---|
| 지금 판단에 꼭 필요한가? | `L1` | model이 직접 reasoning할 최소 context |
| 반복 계산·filter에 필요한가? | `L2` | Python object와 tool result를 재사용 |
| restart 뒤에도 필요한가? | `L3` | history, memory, skill, specification으로 보존 |
| 일반 능력 자체를 바꿔야 하는가? | `L0` | Prime Agent `/refine` 범위 밖; training 문제 |

### Context admission rule

```python
def compact_evidence(records, limit=20):
    """Return only decision-relevant evidence for active context."""
    ranked = sorted(records, key=lambda x: x["severity"], reverse=True)
    return [
        {"path": x["path"], "severity": x["severity"], "reason": x["reason"]}
        for x in ranked[:limit]
    ]
```

출력 전 “이 object 전체가 현재 판단에 필요한가?”를 묻는다. REPL state가 무한히 깨끗한 것은 아니므로 stale variable, secret, huge object의 lifecycle도 관리한다.

## 2. Recursive Delegation Design

`rlm()`은 단순 병렬 호출이 아니라 child마다 독립 context, kernel, history를 만드는 recursive boundary다.

### Good task contract

```python
child = await rlm(
    """
    Goal: Inspect authentication code for concrete security risks.
    Scope: src/auth/** and tests/auth/** only.
    Constraints: Read-only; do not access network or credentials.
    Evidence: Cite file paths and relevant symbols.
    Deliverable: Maximum five findings, each with severity and a testable remediation.
    Stop: Return early if the scoped paths do not exist.
    """,
    name="auth-reviewer",
)
```

Task contract에는 goal, scope, constraints, evidence, deliverable, stop condition을 넣는다. Parent가 다시 전체 trajectory를 읽지 않도록 compact artifact schema를 정한다.

```json
{
  "status": "done",
  "findings": [
    {"path": "src/auth/session.ts", "symbol": "rotate", "severity": "high", "reason": "..."}
  ],
  "unknowns": [],
  "tests_run": []
}
```

### Concurrency control

- child 수보다 **검증 가능한 독립 workstream 수**를 먼저 센다.
- sibling이 같은 file을 수정하지 않도록 ownership을 나눈다.
- root가 evidence를 합성하고 contradiction을 해결한다.
- token, cost, wall time, turn과 child depth/concurrency를 모두 제한한다.
- completion message가 없어도 timeout·crash·partial artifact를 판정할 수 있게 한다.

## 3. Durable Objective Loop

```text
/goal
  ↓
worker + persistent kernel
  ↓ heartbeat/schedule
observe → plan → act → verify → checkpoint
  ↑                              ↓
reattach ← daemon/session catalog
```

Durability는 correctness를 보장하지 않는다. 오래 실행되는 잘못된 loop를 막기 위해 `/autonomous`에 budget와 quality gate를 함께 둔다.

권장 gate:

- immutable acceptance test 통과
- external verifier가 artifact를 독립 검사
- destructive action과 credential access는 human approval
- progress가 없는 N turn 뒤 stop
- cost/time threshold에서 checkpoint 후 종료

## 4. Refinement Lifecycle

```text
trajectory
   ↓ analyze repeated success/failure
candidate typed-state diff
   ↓ review against objective and security policy
versioned apply
   ↓ canary task + immutable verifier
keep ─────────────── or rollback
```

### Typed state decision

| 발견 | 저장 대상 | 예시 |
|---|---|---|
| 반복 행동 규칙 | prompt note | “수정 전 scoped test를 먼저 실행한다.” |
| 교정된 안정적 사실 | memory | “이 repo의 auth entry point는 X다.” |
| 재현 가능한 절차 | skill | lint→test→artifact 검증 순서 |
| 반복 분업 패턴 | subagent specification | read-only security reviewer 역할 |

### Do not refine blindly

Factorio 사례처럼 agent가 reward function의 허점을 이용하고 `/refine`이 이를 skill로 보존할 수 있다. 다음 항목은 자동 승인하지 않는다.

- verifier를 우회하거나 test를 약화하는 변경
- credential, network, filesystem scope 확대
- reward를 높이지만 실제 objective를 훼손하는 shortcut
- 출처가 불명확한 package/skill 설치
- “항상 성공으로 간주” 같은 evidence 제거 규칙

### Review template

```markdown
## Refinement Review

- Triggering trajectories:
- State type:
- Proposed diff:
- Intended benefit:
- Possible exploit/reward hacking:
- Security scope change:
- Canary tasks:
- Immutable verifier result:
- Decision: accept / revise / rollback
```

## 5. Benchmarking Harness Effects

Harness 비교는 동일 model 이름만 맞춰서는 부족하다.

- [ ] exact model snapshot과 provider
- [ ] system prompt와 available tools
- [ ] context/compaction policy
- [ ] task timeout, token/cost budget
- [ ] child concurrency와 retry
- [ ] environment와 dependency version
- [ ] evaluator, hidden test, Best@k calculation
- [ ] raw trajectories와 failure classification
- [ ] confidence interval과 multiple seeds/runs

특히 `Best@3`는 세 번의 비용과 selection effect를 포함한다. `Best@1`과 직접 동일 비용으로 읽지 않는다.

## 6. Threat Model

| 위협 | 예시 | 방어선 |
|---|---|---|
| arbitrary code execution | generated Python/shell이 host file 변경 | disposable container, least privilege |
| secret exposure | REPL이 environment variable 읽음 | secret 미주입, scoped credential broker |
| network exfiltration | package/tool이 외부 전송 | egress allowlist, audit log |
| reward hacking | verifier 허점을 이용 | immutable external test, adversarial review |
| refinement poisoning | exploit을 memory/skill로 저장 | diff approval, provenance, canary, rollback |
| runaway recursion | child가 child를 무한 생성 | depth/concurrency/cost/time limit |
| stale state | 오래된 L2/L3 사실 재사용 | timestamp, invalidation, session hygiene |

## Completion Criteria

- [ ] L1 admission rule과 L2/L3 retention rule을 문서화했다.
- [ ] child contract와 artifact schema를 정의했다.
- [ ] root/descendant budget과 depth limit을 설정했다.
- [ ] immutable verifier가 agent write scope 밖에 있다.
- [ ] refinement review와 rollback을 실제로 시험했다.
- [ ] benchmark claim과 independent reproduction을 구분했다.

## Sources

- [Prime Agent 기술 논문](https://arxiv.org/html/2608.23552)
- [RLM Runtime Architecture](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/rlm-runtime.md)
- [Architecture documentation index](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/index.md)
- [Refine skill](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/skills/refine/SKILL.md)
- [Continual Harness 논문](https://arxiv.org/abs/2605.09998)

