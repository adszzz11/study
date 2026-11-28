---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 실행 방식과 계층 비교

## 비교의 범위

제공 자료에는 직접적인 경쟁 제품 benchmark가 없다. 아래는 역할과 적용 조건의 비교이며 제품 성능 순위가 아니다.

| 대상 | 성격 | AX와의 관계 | 검토 질문 |
|---|---|---|---|
| Stateless microservice | 상태 없는 service | AX는 상태가 누적되는 agent 실행 중심 | 중단·재개와 작업 상태가 필요한가? |
| Run-to-completion batch job | 완료 후 종료 | agent에는 중간 대기와 tool/model 호출이 있을 수 있음 | 완료까지 연속 실행으로 충분한가? |
| Kubernetes | 선언형 cluster 운영 기반 | AX CLI는 kubectl 형태, Kubernetes context 연동 | 기존 cluster 운영에 통합할 것인가? |
| Agent Substrate | actor·sandbox·snapshot·network 실행 기반 | AX의 하위 실행 계층 | 저수준 실행 API만 필요한가? |
| Prebuilt agent images | Antigravity 등을 포함한 agent workload | AX가 조율하는 실행 대상 | 준비된 image와 custom runner 중 무엇이 필요한가? |
| AX Studio / CLI | 동일 AX의 두 interface | local web app과 manifest/명령 중심 운영 | 관찰과 반복 자동화 중 무엇이 중요한가? |

## 선택 관점

AX의 차별점은 새로운 reasoning algorithm보다 agent 실행의 운영 추상화에 있다. prompt와 model 품질은 별도로 평가해야 한다.

- 단순 작업이면 기존 service/job의 운영 비용과 먼저 비교한다.
- 상태를 보존하는 격리 실행이 필요하면 AX와 Substrate의 역할을 함께 검토한다.
- production 도입 전에는 API 안정성·장애 복구·비용 통제·보안 경계를 실측한다.
- local에서 remote로 옮기는 `promote`는 연결 resource를 복사하고 대상 cluster에서 resume한다. memory state의 live migration으로 해석하지 않는다.

## 다음 읽기

[[tech/ai/agent-executor-runtime-5e864373/04-learning/02-deep-dive|설계 경계 심화]] · [[tech/ai/agent-executor-runtime-5e864373/README|학습 진입점]]

## Sources

- https://github.com/google/ax — 제공 dossier의 원 출처 저장소. 본 노트는 dossier 기반이며 현재 원격 저장소와 대조하지 않았다.
- https://github.com/google/ax/releases — 설치 버전과 runner 호환 조건 확인 위치. 수집 예시 `v0.4.0-rc.2`를 최신 버전으로 간주하지 않는다.
