---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 격리·상태·운영

## 1. 보안 경계 검증

실험용 Actor와 승인된 테스트 endpoint만 사용한다.

- 허용되지 않은 outbound, Actor 간 lateral access, control plane 접근이 차단되는지 확인한다.
- 허용 endpoint 호출에서 gateway가 credential을 주입하는지 확인한다. credential 원문을 출력하거나 로그에 남기지 않는다.
- sandbox 내부 identity 인식과 credential 직접 보유를 구분한다.
- 사용하는 HTTP client·TLS·protocol에서 interception이 동작하는지 확인한다.

판정 기준은 허용 요청 성공과 비허용 요청 차단을 함께 관찰하는 것이다. Prompt-injection scanning이나 DLP는 별도 PEP 통합 없이는 기본 기능으로 가정하지 않는다.

## 2. Snapshot과 Teleport

메모리 Counter와 임시 파일을 함께 갱신한 뒤 suspend·resume한다. 전후 값을 비교하고 Worker 식별 정보도 기록한다. Shell session·coding environment처럼 process state가 있는 예제로 확장할 수 있다.

외부 연결·진행 중인 tool 호출은 별도 관찰한다. 재시도에는 request ID·idempotency key·외부 상태 조회가 필요할 수 있으며, 이는 애플리케이션 설계 과제다.

## 3. Request Parking과 포화

WorkerPool보다 많은 동시 요청을 보내 router의 대기 동작을 관찰한다. 즉시 `503`을 반환하는 대신 Worker 확보까지 기다리는 구조이므로 성공률만으로 평가하지 않는다.

| 축 | 측정 항목 |
|---|---|
| 부하 | 등록 Actor 수·동시 활성 비율·요청 간격 |
| 자원 | Worker 수·CPU·RAM·snapshot I/O |
| 응답 | p50/p95/p99 latency·parking 시간·timeout·오류율 |
| 복원 | snapshot 크기·restore 시간·backend |

연속 CPU 부하와 대기 중심 부하를 나누어 측정한다. 프로젝트의 oversubscription 수치와 비교할 때 baseline과 측정 조건을 먼저 맞춘다.

## 4. 운영 관찰점

- `ateapi`·`atecontroller`: lifecycle과 reconciliation 상태.
- `atelet`·backend: Worker 감독, checkpoint·restore, 상태 전송 실패.
- router·egress: routing·parking·policy 거부·upstream timeout.
- identity·storage: 인증 검증, snapshot 접근 통제·보관·삭제 정책.

Snapshot은 메모리와 파일을 포함하므로 민감 데이터가 들어갈 수 있다. 암호화·보존 기간·접근 권한의 구체적 제공 범위는 원문과 배포 구성을 확인한다.

## Navigation

- [[tech/infra/agent-substrate-runtime-a5ffcd0a/README|학습 진입점]]

## Sources

- https://github.com/agent-substrate/substrate
- 작성 근거: 사용자 제공 dossier. 원문 checkout 및 실행 검증은 수행하지 않았다.
