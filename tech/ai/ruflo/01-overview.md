---
date: 2026-09-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Ruflo: What, Why, Architecture

> [[README|목차]] · [[02-ecosystem|다음: 생태계]]

## What

Ruflo는 coding agent가 실제 repository에서 일하는 과정을 감싸는 local-first orchestration layer다. CLI와 MCP를 통해 swarm, workflow, memory, hooks, security 기능을 제공하고 Claude, OpenAI, Gemini, local LLM을 실행 대상 또는 routing 후보로 활용한다.

`Claude Flow`라는 이름으로 개발되다가 2026-02-27 v3.5에서 Ruflo로 공식 rebranding되었다. 따라서 오래된 문서·package scope·경로에 `claude-flow` 이름이 남아 있을 수 있다.

## Why

| 일반 coding agent의 문제 | Ruflo의 접근 |
|---|---|
| 한 model/context에 research·coding·test가 집중됨 | specialized agent와 swarm topology로 역할 분해 |
| session 종료 후 성공 pattern이 소실됨 | AgentDB/RuVector 기반 persistent memory |
| 동시 agent의 역할·공유 상태·결과 취합이 어려움 | coordinator, workflow, shared state |
| tool/shell/file operation의 통제가 제각각임 | hooks, guidance, deterministic gateway, audit |
| client마다 MCP·memory·hook 설정을 반복함 | meta-harness와 plugin layer에서 통합 |

핵심 가치는 “더 많은 agent” 자체가 아니라 **분해할 가치가 있는 작업만 분해하고, 실행 결과를 검증하며, 다음 작업에 재사용하는 loop**에 있다.

## 핵심 구성

### CLI와 MCP

- `npx ruflo ...` CLI: 초기화, 진단, swarm, memory, workflow 운영
- MCP server: coding agent가 Ruflo capability를 tool로 호출
- core plugin 문서 기준 314개 MCP tools를 다루지만 전부 노출하기보다 필요한 namespace만 선택하는 것이 안전하다.

### Multi-agent swarm

| Topology | 구조 | 적합한 작업 |
|---|---|---|
| `mesh` | peer-to-peer | 소규모 탐색, 상호 검토 |
| `hierarchical` | coordinator/queen 중심 | 역할과 승인선이 명확한 대형 작업 |
| `hierarchical-mesh` | 계층 제어 + peer 협업 | 일반적인 복합 개발 작업 |
| `adaptive` | workload에 따라 변경 | task 성격이 자주 달라지는 경우 |

Configuration 문서의 기본값은 `hierarchical-mesh`, 최대 agent 수는 15다. 이는 안전한 권장 동시성이라는 뜻이 아니며 repository 충돌, API rate limit, token budget에 맞춰 낮춰야 한다.

### Specialized agents와 workflow

공식 README의 full CLI snapshot에는 98 agent definitions, 60개 이상 commands, 30 skills, MCP server, hooks, daemon, SPARC와 reusable workflow가 포함된다. `coder`, `reviewer`, `tester`, `researcher`, `security-architect`처럼 책임을 분리한다. 이 숫자들은 API contract가 아니라 release snapshot이다.

### Persistent memory

- SQLite, AgentDB 또는 hybrid backend
- HNSW semantic retrieval과 RuVector
- RAG, graph traversal, embedding·quantization plugin
- session 간 task result, trajectory, success pattern 재사용
- RVF 기반 memory/session portability

단순 chat history 저장과 달리 과거 trajectory를 retrieval과 routing feedback에 쓰려는 것이 목표다. 다만 “150× search”, “self-learning” 같은 표현은 project 자체 benchmark이므로 독립 검증된 보편적 성능으로 해석하지 않는다.

### Hooks와 learning loop

```text
PreToolUse → tool/policy 검사 → 실행 → PostToolUse
     ↓                              ↓
 routing                         result 저장
     └──── RETRIEVE → JUDGE → DISTILL → CONSOLIDATE ────┘
```

`PreCompact`는 context compaction 전 memory 보존, `Stop`은 session 결과 정리 등에 활용된다. hook은 자동화 지점인 동시에 privilege escalation과 data leakage 지점이므로 입력·출력·side effect를 함께 감사해야 한다.

### Guidance Control Plane

| Component | 역할 |
|---|---|
| `GuidanceCompiler` | 자연어 지침을 constitution과 task shard로 분해 |
| `EnforcementGates` | destructive operation, secret, diff size, allowlist 검사 |
| `DeterministicToolGateway` | schema, idempotency, budget, policy gate |
| `ContinueGate` | continue/checkpoint/throttle/pause/stop 결정 |
| `ProofChain` | hash-chained event 기록 |
| `MemoryWriteGate` | namespace 권한과 contradiction 검사 |
| `TrustSystem` / `AuthorityGate` / `ThreatDetector` | trust·authority·threat 판단 |

Rust/WASM kernel과 JavaScript fallback을 지향하지만 subsystem maturity가 동일하다고 가정하면 안 된다. top-level package가 stable이어도 내부 manifest에는 `3.0.0-alpha.*` dependency가 있어 component별 검증이 필요하다.

## 장점과 한계

| 장점 | 한계/위험 |
|---|---|
| coding workspace 중심의 통합된 orchestration | 작은 task에는 coordination 비용이 큼 |
| CLI와 MCP를 모두 제공 | 방대한 tool surface가 context와 보안 부담을 만듦 |
| session을 넘는 semantic memory | stale/poisoned memory와 privacy 관리 필요 |
| plugin으로 기능을 선택 가능 | full CLI와 plugin별 command/tool 이름이 다를 수 있음 |
| policy와 audit를 architecture에 포함 | 문서상 설계와 실제 enforcement를 test해야 함 |

## Sources

- https://github.com/ruvnet/ruflo/blob/main/README.md
- https://github.com/ruvnet/ruflo/blob/main/CHANGELOG.md
- https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-core/README.md
- https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agentdb/README.md
- https://github.com/ruvnet/ruflo/blob/main/SKILL.md
- https://github.com/ruvnet/ruflo/blob/main/v3/%40claude-flow/guidance/docs/guides/architecture-overview.md

