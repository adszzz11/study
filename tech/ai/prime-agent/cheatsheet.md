---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Prime Agent — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차]]

## Mental Model

```text
L0 model weights
L1 active token context
L2 persistent REPL objects + tool results + recursive subagents
L3 disk-backed history + memory + skill + prompt note + subagent spec
```

**Rule of thumb**: 계산 가능한 큰 data는 L2에 두고, 재시작 뒤 필요한 지식·절차는 검토 후 L3에 두며, 현재 판단에 필요한 최소 evidence만 L1에 출력한다.

## Architecture

```text
client -> daemon -> AgentSession worker -> Jupyter/ZeroMQ -> IPython kernel
```

| Component | 역할 |
|---|---|
| Client | TUI/CLI/RPC interaction과 event 소비 |
| Daemon | durable session catalog, tree, queue, lifecycle |
| Worker | model loop와 TypeScript `AgentSession` |
| Kernel | persistent Python computation/state |

## REPL Patterns

```python
# Filter before print
errors = [line for line in open("build.log") if "ERROR" in line]
print("\n".join(errors[:30]))
```

```python
# Aggregate before context admission
from collections import Counter
counts = Counter(item["kind"] for item in records)
print(counts.most_common(10))
```

```python
# Recursive child: admission returns a stable handle
child = await rlm(
    "Inspect auth code read-only; cite paths/symbols; return at most five findings.",
    name="auth-reviewer",
)
print(child.rlm_child_id, child.model)
```

## Operational Commands

| Command | 목적 | 핵심 주의점 |
|---|---|---|
| `/goal` | durable objective 설정 | measurable stop condition 포함 |
| `/heartbeat` | 장기 task 재진입 | progress 없는 loop 제한 |
| `/autonomous` | budget·quality gate를 둔 자율 실행 | 외부 verifier 필수 |
| `/refine` | typed harness state 개선 | weights 학습 아님; diff review |
| `/fork` | session 분기 | lineage와 cost 기록 |
| `/clone` | session 복제 | stale state·secret 복제 점검 |

명령 option은 release에 따라 바뀔 수 있으므로 [Architecture documentation index](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/index.md)에서 확인한다.

## Child Task Contract

```text
Goal:
Scope:
Constraints:
Evidence required:
Deliverable/schema:
Stop condition:
Budget:
```

## Refinement Types

| State | 저장할 것 | 저장하지 말 것 |
|---|---|---|
| prompt note | 반복 행동 규칙 | 일회성 task detail |
| memory | 검증된 재사용 사실 | 추측·만료된 사실·secret |
| skill | 재현 가능한 executable procedure | verifier 우회·출처 불명 code |
| subagent specification | 반복되는 역할·분업 contract | 과도하게 넓은 권한 |

```text
trajectory -> candidate diff -> human/security review
           -> canary + immutable verifier -> keep or rollback
```

## Provider Options

- Subscription: Claude, ChatGPT/Codex, GitHub Copilot
- API key: OpenAI, Anthropic, Gemini, Bedrock, DeepSeek, Mistral, Groq, OpenRouter, Prime Inference 등
- Local: Ollama, vLLM, LM Studio 등 OpenAI-compatible endpoint + `models.json`

지원 여부와 exact model ID는 [Coding Agent README](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/README.md)와 [Custom Models](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/models.md)에서 재확인한다.

## Safety Checklist

- [ ] disposable clone/container
- [ ] filesystem·network least privilege
- [ ] production credential 미주입
- [ ] immutable external acceptance test
- [ ] third-party package/skill source allowlist
- [ ] refinement provenance·diff review·rollback
- [ ] token·cost·time·turn budget
- [ ] child depth·concurrency limit
- [ ] destructive action human approval
- [ ] stale L2/L3 state invalidation

> [!danger] Daemon/worker/kernel 분리는 security sandbox가 아니다. Generated Python과 shell은 현재 사용자 권한으로 실행된다.

## Benchmark Reading

- `95.5% RHAE Best@1`, `[95.0, 95.2, 95.5]`, `99.97% Best@3`는 개발진 보고 수치다.
- Best@k는 총 실행 비용과 selection protocol을 함께 본다.
- model, provider, harness version, budget, concurrency, evaluator를 고정한다.
- confidence interval, multiple runs, raw trajectory, independent reproduction을 확인한다.
- nanoGPT에서 harness effect가 noise보다 작았다는 저자 보고도 함께 고려한다.

## Quick Decision

| Use | Avoid |
|---|---|
| long-context filtering·aggregation | 짧고 단순한 one-shot task |
| durable long-running session | arbitrary code execution 불가 환경 |
| adaptive recursive delegation | 고정·감사 가능한 DAG 필수 workflow |
| reviewed harness refinement | verifier 없이 자동 refinement |
| cross-provider experiment | 독립 검증된 안정성이 즉시 필요한 production |

## Sources

- [Prime Agent 공식 저장소](https://github.com/PrimeIntellect-ai/prime-agent)
- [Prime Agent 기술 논문](https://arxiv.org/html/2608.23552)
- [RLM Runtime Architecture](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/rlm-runtime.md)
- [Refine skill](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/skills/refine/SKILL.md)

