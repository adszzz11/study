---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: AX를 평가하는 작은 실험

## Project 1 — Lifecycle 관찰

- **목표:** apply와 실행 시작의 분리, 상태 보존 확인.
- **절차:** 단일 Task로 로컬 파일에 진행 표시를 남기고 suspend/resume 전후를 비교한다.
- **산출물:** release·image digest·Git ref·명령·시각·관찰 상태 표.
- **완료 기준:** `Suspended` 초기 상태와 resume 후 준비 과정을 설명하고 CLI timeout을 workload 실패와 구분한다.

## Project 2 — Gateway 최소 접근 정책

- **목표:** host 제한과 credential injection의 실제 동작 확인.
- **절차:** 실습용 허용 host와 차단 host에 요청하고, 폐기 가능한 credential로 인증을 확인한다.
- **산출물:** 정책별 요청 결과와 secret 노출 여부를 기록한 표. 실제 secret은 기록하지 않는다.
- **완료 기준:** 허용·차단 사례를 관찰하고 자료에서 확인되지 않은 우회 방지나 tenant 경계를 보장한다고 쓰지 않는다.

## Project 3 — 중복 호출과 복원

- **목표:** checkpoint와 외부 side effect의 차이 이해.
- **절차:** mock API에 요청 ID를 기록하고 suspend/resume 전후 호출 횟수를 비교한다. idempotency key 적용 전후를 비교한다.
- **산출물:** 호출 순서·중복 수·재실행 시점 기록.
- **완료 기준:** 관찰 결과와 보장 수준을 분리한다. 한 번 중복이 없었다는 결과로 exactly-once를 주장하지 않는다.

## Project 4 — 환경 이동과 입력 고정

- **목표:** promote의 범위와 재현성 한계 평가.
- **절차:** 연습용 cluster 두 개에서 동일 image digest·Git commit을 사용한다. 현재 release 문법으로 promote하고 대상 resource와 실행 상태를 확인한다.
- **산출물:** context별 resource 목록, 입력 버전, 결과 차이.
- **완료 기준:** resource 복사와 memory live migration을 구분하고 model/tool 변동을 설명한다.

## 평가 기록 틀

| 가설 | 고정한 입력 | 관찰 결과 | 미확인 사항 | 후속 검증 |
|---|---|---|---|---|
| 예: resume 후 파일 상태 유지 | release, digest, Git commit | 실습 후 기입 | 장애 시 복구 보장 | 실패 주입 조건 별도 설계 |

모든 프로젝트는 연습용 환경에서 수행한다. 수백만 task 규모 검증은 이 소규모 실습의 결과로 대체할 수 없다.

## 연결

[[tech/ai/agent-executor-runtime-5e864373/04-learning/01-getting-started|시작하기]] · [[tech/ai/agent-executor-runtime-5e864373/04-learning/02-deep-dive|검증할 설계 경계]] · [[tech/ai/agent-executor-runtime-5e864373/README|학습 진입점]]

## Sources

- https://github.com/google/ax — 제공 dossier의 원 출처 저장소. 본 노트는 dossier 기반이며 현재 원격 저장소와 대조하지 않았다.
- https://github.com/google/ax/releases — 설치 버전과 runner 호환 조건 확인 위치. 수집 예시 `v0.4.0-rc.2`를 최신 버전으로 간주하지 않는다.
