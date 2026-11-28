---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화 학습: 실행과 보장의 경계

## 1. Resource와 실행 책임 추적

Task 목표 → Workspace 준비 → Substrate actor 배치 → sandbox 실행 경로를 그린다. Gateway 선언이 실제 egress·credential injection 집행으로 연결되는 지점을 확인한다.

공통 Workspace를 여러 Task에서 참조하는 것과 파일을 안전하게 공유하는 것은 다른 문제다. 제공 자료에는 파일 공유·동시성·충돌 처리 규칙이 없으므로, 별도 검증 전 공유 방식에 의존하지 않는다.

## 2. 상태 복원과 외부 side effect

```text
외부 API 호출 성공
       |
       +-- checkpoint 전 중단/실패 가능성 검토
       |
resume 후 호출 재실행 가능 여부 확인
```

actor checkpoint가 외부 시스템의 transaction과 원자적으로 묶인다는 근거는 없다. 실습에서는 모의 API와 idempotency key를 사용해 중복을 관찰한다. suspend/resume이 exactly-once를 보장한다고 쓰지 않는다.

`promote`는 다른 Kubernetes context의 cluster에 Task 및 연결 resource를 복사한 뒤 resume한다. 실행 중 memory의 live migration 여부는 별도 확인 대상이다.

## 3. 재현성과 Runner contract

- image digest는 image 변경을 막는 기반이다.
- Git branch는 이동할 수 있으므로 commit SHA도 기록한다.
- model 버전·sampling 설정·tool 응답은 결과 변동 요인이다.
- custom runner image는 control plane과 task container 사이 contract를 충족해야 한다.
- prebuilt image는 release notes의 runner volume image 요구사항을 확인한다. 상세 contract는 dossier만으로 구현할 수 없다.

## 4. 보안 검증

| 검증 축 | 관찰할 내용 | 자료만으로 단정하지 않을 것 |
|---|---|---|
| Sandbox / resource limit | CPU·memory 제한과 실패 처리 | 구체적인 multi-tenant 보안 경계 |
| Egress | 허용/차단 host 접근 결과 | 모든 우회 경로 차단 |
| Credential injection | 필요한 요청에서 인증 성공, 로그 노출 여부 | 모든 agent action의 완전한 감사 |
| Lifecycle | 상태 복원과 장애 로그 | checkpoint 주기와 복구 SLA |

Gateway는 agent가 credential을 직접 보지 않고 필요한 접근을 수행하도록 소개된다. 실제 secret 노출 가능 경로는 실습 환경에서 별도로 검토한다.

## 5. Observability

`ax-server` 관측 범위에는 logs·metrics·traces·events가 있다. CLI의 `--trace`는 trace ID를 출력하고 RPC에 sampled W3C `traceparent`를 전달한다. `OTEL_EXPORTER_OTLP_ENDPOINT`가 설정되면 CLI span을 OTLP로 export한다.

- CLI trace와 server 관측을 연계해 초기화 지연과 실행 실패를 구분한다.
- trace 존재를 모든 tool/model 호출의 감사 보장으로 확대 해석하지 않는다.
- token·비용 hard budget과 자동 차단은 제공 자료에서 확인되지 않았다.

## 다음 실습

[[tech/ai/agent-executor-runtime-5e864373/05-projects|검증 프로젝트]] · [[tech/ai/agent-executor-runtime-5e864373/README|학습 진입점]]

## Sources

- https://github.com/google/ax — 제공 dossier의 원 출처 저장소. 본 노트는 dossier 기반이며 현재 원격 저장소와 대조하지 않았다.
- https://github.com/google/ax/releases — 설치 버전과 runner 호환 조건 확인 위치. 수집 예시 `v0.4.0-rc.2`를 최신 버전으로 간주하지 않는다.
