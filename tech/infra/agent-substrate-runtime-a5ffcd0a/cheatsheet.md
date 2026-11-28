---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Substrate Cheatsheet

## 핵심 구분

| 질문 | 빠른 답 |
|---|---|
| 무엇인가? | Kubernetes 위 stateful sandbox runtime |
| 무엇을 분리하나? | Actor의 상태·정체성과 Worker의 실행 자원 |
| 실행 경계는? | gVisor(`runsc`) 또는 Cloud Hypervisor microVM |
| plain container는? | Actor backend로 미지원; OCI image 입력과 구분 |
| snapshot 대상은? | RAM과 filesystem |
| Actor Teleport는? | suspend 후 다른 가용 Worker에서 resume |
| Request Parking은? | Worker 포화 시 router에서 요청 대기 |
| credential은 어디에? | sandbox 외부, 승인된 요청에 egress gateway가 주입 |
| 네트워크 기본값은? | default-deny, inbound router·outbound gateway |
| identity는? | Actor·Atespace 기반, SPIFFE X.509와 정책에 따른 JWT |
| SDK 대체인가? | 아니다. ADK·LangChain 등과 조합하는 실행 계층 |

## 수치 읽기

- <500ms resume, >500 activation/s, 10배 밀도, 10–30배 oversubscription: **프로젝트 주장**.
- 약 250 Actor / 8 physical Pod: demo 범위.
- 측정 환경·부하 분포·percentile·baseline 상세가 없어 자체 검증 필요.

## 운영 시 기억할 것

- 대기 중심 workload에서 Worker 공유 이점이 커진다.
- PEP 확장 가능성이 DLP·scanning의 기본 제공을 뜻하지 않는다.
- MITM interception의 protocol·client 지원 범위를 확인한다.
- Snapshot 복원은 외부 연결 생존·exactly-once 보장이 아니다.
- Parking은 실패를 대기로 바꾸므로 timeout과 tail latency를 본다.

## 문제 추적

```text
요청 지연 → router parking → WorkerPool ready/포화
복원 실패 → atelet → backend checkpoint/restore → snapshot storage
외부 호출 실패 → egress policy → interception 호환성 → upstream
인증 실패 → Actor/Atespace identity → 인증서/JWT 검증 구성
```

이는 진단 순서 제안이며, 특정 log 필드나 CLI 명령을 보장하지 않는다.

## Navigation

- [[tech/infra/agent-substrate-runtime-a5ffcd0a/README|학습 진입점]]

## Sources

- https://github.com/agent-substrate/substrate
- 작성 근거: 사용자 제공 dossier. 원문 checkout 및 실행 검증은 수행하지 않았다.
