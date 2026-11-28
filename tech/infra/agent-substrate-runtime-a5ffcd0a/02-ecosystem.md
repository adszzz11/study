---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem과 비교

## Runtime의 위치

Substrate는 모델 호출·추론 흐름·tool orchestration을 설계하는 SDK를 대체하기보다, 그 코드를 실행할 환경을 제공한다. 아래 비교는 dossier에 직접 언급된 기술에 한정한다.

| 기술·방식 | 관계 | 선택·조합 관점 |
|---|---|---|
| 일반 Linux container | 보안·밀도 비교 대상 | Actor backend로 미지원; gVisor 또는 microVM 필수 |
| Kubernetes | 기반 | Pods·autoscaling·NetworkPolicies에 Actor scheduling·snapshot·identity 추가 |
| gVisor | sandbox backend | `runsc` checkpoint·restore 경로 |
| Cloud Hypervisor microVM | sandbox backend | VM 경계; gVisor와 정량 비교 자료 없음 |
| ADK·LangChain | 상위 agent framework | 작성한 agent 코드를 실행 환경과 조합 |
| Claude Code·Codex·Antigravity | coding workload | 프로세스·filesystem 상태를 이어가는 격리 환경 |
| MCP | sandboxed server 배포 대상 | Actor로 실행하며 identity·egress 통제 적용 |
| Agent Executor | Substrate 위 distributed agent runtime 사례 | 대규모 agent harness 구현 예시 |
| kagent | Kubernetes-native framework, CNCF Sandbox 프로젝트 | sandboxed stateful workload 실행에 Substrate 활용 |

## 선택 기준

- 기존 Kubernetes 구성만으로 충분한지, Actor snapshot·resume이 필요한지 먼저 판단한다.
- backend 선택은 실제 workload의 compatibility·resume latency·운영 비용으로 검증한다. 자료에는 backend 간 우열을 정할 수치가 없다.
- 상위 framework와 runtime의 책임을 분리해 평가한다.
- CNCF Sandbox 표기는 **kagent**에 관한 설명이다. Substrate 자체의 CNCF 지위를 확정하지 않는다.

## Navigation

- [[tech/infra/agent-substrate-runtime-a5ffcd0a/README|학습 진입점]]

## Sources

- https://github.com/agent-substrate/substrate
- 작성 근거: 사용자 제공 dossier. 원문 checkout 및 실행 검증은 수행하지 않았다.
