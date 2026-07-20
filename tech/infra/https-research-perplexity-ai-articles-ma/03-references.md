---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# SPACE References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## Primary Source

### Perplexity Research — Making SPACE

- URL: https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents
- 공개일: 2026-07-15
- 읽을 부분:
  - 3-layer architecture와 reconciliation
  - VM + host process isolation, controlled channel
  - external credential store, egress injection, BYOK
  - disk/full snapshot, suspend transaction, cross-node restore
  - btrfs reflink, warm pool, request coalescing
  - production latency 결과
- Evidence 성격: 설계와 수치는 **vendor-authored production report**다. architecture 학습에는 직접 근거이지만 독립 benchmark나 security audit는 아니다.

## Agent Workload와 Kubernetes

### Kubernetes SIG Apps — Running Agents on Kubernetes with Agent Sandbox

- URL: https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/
- 핵심: agent를 isolated, stateful, singleton workload로 정의하고 `Sandbox` CRD, stable identity, scale-to-zero, `SandboxWarmPool`을 설명한다.
- 비교 포인트: SPACE의 내부 control plane과 Kubernetes-native abstraction이 해결하려는 lifecycle 문제가 유사하다.
- 주의: 글 시점 project는 in development이며 latest release와 backend semantics를 별도 확인해야 한다.

### Kubernetes SIGs Agent Sandbox Repository

- URL: https://github.com/kubernetes-sigs/agent-sandbox
- 용도: 실제 CRD, controller, extension, release 상태 확인

## Sandbox Providers

### E2B Persistence

- URL: https://e2b.dev/docs/sandbox/persistence
- 핵심: filesystem과 memory를 보존하는 pause/resume, auto-pause, lifecycle state

### E2B Snapshots

- URL: https://e2b.dev/docs/sandbox/snapshots
- 핵심: one-to-one pause/resume와 one-to-many snapshot fork의 차이

### Daytona Sandboxes

- URL: https://www.daytona.io/docs/en/sandboxes/
- 핵심: container/VM의 stop, pause, archive, recover semantics 차이

### Daytona Snapshots

- URL: https://www.daytona.io/docs/en/snapshots/
- 핵심: container cold snapshot과 VM memory 포함 hot snapshot

## Isolation Primitives

### gVisor Architecture and Security

- URL: https://gvisor.dev/docs/architecture_guide/intro/
- URL: https://gvisor.dev/docs/architecture_guide/security/
- 핵심: userspace application kernel로 host kernel 공격면을 줄이는 모델과 보호하지 않는 영역

### Firecracker

- URL: https://firecracker-microvm.github.io/
- URL: https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md
- 핵심: minimal device model의 microVM VMM. SPACE와 동일 구현이라는 근거는 없으며 VM isolation primitive의 참고 자료다.

### Kata Containers

- URL: https://katacontainers.io/
- URL: https://github.com/kata-containers/kata-containers
- 핵심: lightweight VM isolation을 container ecosystem에 연결하는 runtime

## Storage와 Snapshot

### btrfs Documentation

- URL: https://btrfs.readthedocs.io/en/latest/Reflink.html
- URL: https://btrfs.readthedocs.io/en/latest/Subvolumes.html
- 핵심: reflink/CoW와 subvolume snapshot의 filesystem semantics

> [!note] Consistency 주의
> filesystem snapshot이 atomic하다는 말은 application의 in-memory buffer, open transaction, 외부 side effect까지 일관되다는 뜻이 아니다. crash-consistent와 application-consistent snapshot을 구분한다.

## Durable Workflow — 다른 계층

### Temporal Documentation

- URL: https://docs.temporal.io/
- 핵심: event history와 replay 기반 Durable Execution. VM snapshot과 동일한 문제를 푸는 것이 아니다.

### LangGraph Persistence

- URL: https://docs.langchain.com/oss/python/langgraph/persistence
- 핵심: graph state checkpoint, thread, replay/time-travel. untrusted code isolation은 별도 계층이다.

## Source Evaluation Matrix

| Claim | 가장 직접적인 source | 검증 상태/한계 |
|---|---|---|
| SPACE 3계층과 security model | Perplexity 원문 | first-party architecture description |
| 60 ms median, 89 ms p90 | Perplexity 원문 | vendor internal production measurement |
| agent는 stateful singleton workload | Kubernetes blog | 공식 ecosystem 관점, 일반화에는 환경 차이 존재 |
| E2B memory pause/snapshot | E2B docs | 현재 product documentation |
| Daytona VM/container snapshot 차이 | Daytona docs | 현재 product documentation |
| gVisor dual-kernel model | gVisor docs | project official security description |
| SPACE hypervisor/attestation 세부 | 공개 근거 없음 | 추정 금지 |

## 읽는 순서

1. Perplexity 원문으로 SPACE의 세 목표와 architecture를 잡는다.
2. Kubernetes 글로 workload abstraction을 일반화한다.
3. E2B/Daytona 문서에서 product-level lifecycle semantics를 비교한다.
4. gVisor/Kata/Firecracker로 isolation primitive 차이를 학습한다.
5. btrfs와 durable workflow 문서로 storage checkpoint와 logical checkpoint를 분리한다.

## Sources

- https://research.perplexity.ai/articles/making-space-secure-and-efficient-runtimes-for-long-running-agents
- https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/
- https://github.com/kubernetes-sigs/agent-sandbox
- https://e2b.dev/docs/sandbox/persistence
- https://e2b.dev/docs/sandbox/snapshots
- https://www.daytona.io/docs/en/sandboxes/
- https://www.daytona.io/docs/en/snapshots/
- https://gvisor.dev/docs/architecture_guide/intro/
- https://firecracker-microvm.github.io/
- https://btrfs.readthedocs.io/en/latest/Reflink.html
- https://docs.temporal.io/
- https://docs.langchain.com/oss/python/langgraph/persistence
