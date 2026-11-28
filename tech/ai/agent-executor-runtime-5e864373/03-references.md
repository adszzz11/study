---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 근거와 검증 범위

## 자료 사용 원칙

이 노트 묶음은 사용자 제공 dossier를 정리한 학습 자료다. 원격 repository, release, CLI를 현재 환경에서 직접 검증하지 않았다. dossier는 마지막 문장이 중간에 끝나므로 누락된 내용을 추정해 사실로 추가하지 않았다.

| 확인할 근거 | URL | 확인 목적 |
|---|---|---|
| Repository / README | https://github.com/google/ax | resource model, architecture, lifecycle, maturity |
| Release notes | https://github.com/google/ax/releases | 설치 버전, prebuilt image용 runner volume image 조건 |
| 소스 트리 | https://github.com/google/ax/tree/main | 현재 manifest schema와 runner 관련 구현 탐색; main 변경 가능 |

## 주장별 신뢰 경계

| 주장 | dossier에서 확인되는 수준 | 추가 검증 |
|---|---|---|
| 수백만 task / cluster | 설계 목표 | benchmark, workload 조건, 장애율 |
| Suspend / resume | actor state checkpoint 및 복원 기능 | checkpoint 주기와 장애 시 보장 |
| Gateway | host 제한과 credential injection | 실패 시 차단, redirect, secret 노출 경로 |
| Image digest | 실행 image 고정 기반 | Git commit·tool·model 입력 고정 |
| Promote | 연결 resource 복사 후 대상에서 resume | memory state 이전 여부는 미확인 |
| 비용 통제 | 비용 폭주를 문제로 제시 | hard budget·자동 차단 기능 미확인 |

## 읽을 때 기록할 것

- 열람한 commit SHA, release tag, 열람 날짜를 남긴다.
- README 예제와 CLI help가 다르면 같은 release의 자료로 다시 맞춘다.
- 수집 예시 `v0.4.0-rc.2`는 현재 최신 버전이라는 근거가 아니다.
- 상세 문서 경로를 확인하지 못했으므로 추정 URL을 추가하지 않는다.

## 연결

[[tech/ai/agent-executor-runtime-5e864373/04-learning/01-getting-started|실습 전 확인]] · [[tech/ai/agent-executor-runtime-5e864373/README|학습 진입점]]

## Sources

- https://github.com/google/ax — 제공 dossier의 원 출처 저장소. 본 노트는 dossier 기반이며 현재 원격 저장소와 대조하지 않았다.
- https://github.com/google/ax/releases — 설치 버전과 runner 호환 조건 확인 위치. 수집 예시 `v0.4.0-rc.2`를 최신 버전으로 간주하지 않는다.
