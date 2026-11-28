---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Substrate Overview

## What

Agent SDK 아래, Kubernetes 자원 계층 위에 위치하는 stateful sandbox runtime이다. Actor의 논리적 정체성과 상태를 유지하면서 물리 실행 위치를 바꿀 수 있다.

| 개념 | 역할 |
|---|---|
| Actor | 상태를 가진 논리적 workload |
| Atespace | Actor를 묶는 Substrate namespace, identity에도 포함 |
| ActorTemplate | Actor 실행 구성 template |
| WorkerPool | Worker 자원 풀 |
| Worker | Actor를 실제 실행하는 자원 |
| Snapshot | RAM·filesystem 보존 및 복원 수단 |

## Why

비신뢰 코드를 안전하게 실행하는 문제와 긴 idle 시간의 자원 낭비를 함께 다룬다. 보안 경계는 sandbox가, 논리적 실행 수명은 Actor가 담당한다. **Actor Teleport**는 suspend한 Actor를 pool의 다른 가용 Worker에 resume하는 기능이다.

```text
Inbound → atenet-router → 가용 Worker → Actor sandbox
                 └─ 포화 시 Request Parking
Actor outbound → atenet-egress → 승인된 외부 서비스
Actor idle → RAM + filesystem snapshot → 다음 Worker에서 resume
```

이 흐름은 개념도이며 실제 배포 topology나 API 순서를 확정하지 않는다.

## Components

| 구성요소 | 책임 |
|---|---|
| `ateapi` | gRPC Actor·Worker lifecycle API |
| `atecontroller` | WorkerPool custom resource reconciliation |
| `atelet` | node-level DaemonSet, Worker Pod 감독·snapshot 조율·상태 전송 |
| `atenet` | Envoy routing·proxy sidecar networking controller |
| `atenet-router` | inbound 진입 및 routing |
| `atenet-egress` | outbound policy·외부 credential injection |
| `ateworker-gvisor` | `runsc` checkpoint·restore |
| `ateworker-microvm` | Cloud Hypervisor VM 실행 |
| `ate-idp-server` | JWT 검증용 OpenID discovery·key set |
| `kubectl-ate` | Substrate resource 관리 CLI |

## Security

- 항상 전용 gVisor 또는 microVM에서 실행한다. OCI image 입력 지원은 plain container를 보안 경계로 쓴다는 뜻이 아니다.
- 활성 Actor에는 기본적으로 짧은 수명의 SPIFFE X.509 certificate가 제공된다. egress policy에 따라 gateway가 Actor별 JWT를 발급할 수 있다.
- Actor·Atespace identity와 credential 원문의 sandbox 보유는 별개다. JWT·certificate·API key·cloud token을 비신뢰 코드에 직접 전달하지 않고 외부 gateway가 승인된 요청에 주입한다.
- private network stack·default-deny를 적용한다. inbound는 router, outbound는 egress gateway를 통하며 lateral access·control plane 접근은 차단한다.
- 외부 PEP는 교체 가능하다. 자체 authorization·DLP·prompt-injection scanning·cloud IAM 연결은 확장 지점이며 모두 기본 제공된다는 뜻은 아니다.

## Limits

승인된 API의 오용은 edge policy의 권한·대상·요청 내용 설계로 다뤄야 한다. Header injection 등은 MITM interception에 의존하므로 protocol·client 호환성을 검증한다. Snapshot은 외부 연결 생존이나 외부 작업의 exactly-once semantics를 보장하는 근거가 아니다.

밀도는 동시 활성 Actor 비율에 좌우된다. 지속적인 CPU workload에서 같은 oversubscription을 기대하기 어렵다는 것은 구조적 추론이며 workload별 측정 결과는 아니다.

## Navigation

- [[tech/infra/agent-substrate-runtime-a5ffcd0a/README|학습 진입점]]

## Sources

- https://github.com/agent-substrate/substrate
- 작성 근거: 사용자 제공 dossier. 원문 checkout 및 실행 검증은 수행하지 않았다.
