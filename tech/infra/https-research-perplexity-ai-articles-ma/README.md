---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# SPACE: Secure Runtime for Long-Running Agents

> **한 줄 정의**: **SPACE(Sandboxed Platform for Agentic Code Execution)**는 Perplexity가 long-running, stateful AI agent를 위해 구축한 per-sandbox VM 기반 runtime으로, 강한 격리·상태 snapshot·credential mediation·빠른 복원을 하나의 compute substrate로 결합한다.

## Overview

기존 LLM serving은 짧고 stateless한 inference를 전제로 한다. 반면 agent는 코드를 실행하고 filesystem을 바꾸며, 외부 API나 사람의 승인을 기다린 뒤 같은 작업을 다시 이어간다. SPACE는 이런 workload를 단순한 code interpreter가 아니라 **hostile workload를 격리하면서 pause, move, fork, rollback, recover할 수 있는 stateful runtime**으로 다룬다.

```text
Agent Orchestrator
       │ desired state
       ▼
Stateless Control Plane ── reconcile ── Node-local Services
                                              │ controlled channel
                                              ▼
                                  Per-sandbox VM + space daemon
```

핵심 설계는 다음 세 목표의 균형이다.

- **Security**: untrusted code, prompt injection, credential theft, data exfiltration을 defense in depth로 제한한다.
- **Functionality**: filesystem/process뿐 아니라 pause/resume, suspend/restore, rollback, fork, crash recovery를 제공한다.
- **Efficiency**: btrfs Copy-on-Write(CoW), warm pool, delta snapshot으로 idle agent의 비용과 복원 latency를 줄인다.

> [!warning] 공개 범위
> SPACE는 이 글을 기준으로 Perplexity 내부 production platform이다. 공개 API나 설치 가능한 distribution으로 소개된 것이 아니므로 이 노트의 pseudo code는 architecture 학습용이며 실제 SPACE API가 아니다. 성능과 사용량 수치도 Perplexity 자체 측정값이다.

## Learning Path

- [ ] [[01-overview|1. Overview]] — What/Why, 3계층 구조, security와 snapshot
- [ ] [[02-ecosystem|2. Ecosystem]] — agent sandbox, isolation runtime, workflow runtime 비교
- [ ] [[03-references|3. References]] — primary source와 추가 읽을거리
- [ ] [[04-learning/01-getting-started|4. Getting Started]] — state machine과 failure invariant 설계
- [ ] [[04-learning/02-deep-dive|5. Deep Dive]] — snapshot transaction, credential mediation, recovery 분석
- [ ] [[05-projects|6. Projects]] — 작은 prototype부터 production design review까지
- [ ] [[cheatsheet|7. Cheatsheet]] — 핵심 구조와 점검표 빠른 참조

## When To Use

- agent가 수시간 이상 살아 있고 human-in-the-loop 대기 중 compute를 해제해야 할 때
- 서로 신뢰할 수 없는 tenant의 LLM-generated code를 강하게 격리해야 할 때
- memory, process, filesystem을 함께 보존해 crash recovery나 suspend/resume해야 할 때
- destructive command 직전 checkpoint, rollback, 동일 state에서의 fork가 필요할 때
- credential을 guest에 직접 노출하지 않고 외부 service 접근을 중개해야 할 때
- node failure와 sandbox identity/runtime state를 분리해야 할 때

## When Not To Use

- 짧고 stateless하며 재실행 비용이 낮은 batch job만 처리할 때
- trusted code만 실행하고 filesystem state가 필요 없는 단순 inference endpoint일 때
- workflow의 logical state만 보존하면 충분할 때 — Temporal/LangGraph류 durable workflow가 더 직접적이다.
- process/memory 복원보다 reproducible rebuild가 더 중요한 CI job일 때
- VM, snapshot, KMS, egress gateway를 운영할 platform engineering 역량이 없을 때
- 공개적으로 바로 구매·설치할 sandbox SDK가 필요할 때 — SPACE 자체는 공개 product/API로 문서화되지 않았다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[tech/infra/kubernetes/README|Kubernetes]] — control loop, scheduler, node-local runtime의 기반 개념
- [[tech/infra/prefect/README|Prefect]] — compute sandbox와 구분해야 할 workflow orchestration
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol]] — agent와 tool/data 연결 계층

## Sources

- https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents
- https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/
- https://e2b.dev/docs/sandbox/persistence
- https://www.daytona.io/docs/en/sandboxes/

