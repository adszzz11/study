---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Task Observer — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1: 한 개 skill로 2주 pilot

### 목표

Task Observer의 가치와 운영 비용을 작은 범위에서 검증한다.

### 범위

- 반복 사용되는 target skill 1개
- stable workspace 1개
- 실제 task 5회 이상
- review 1회

### 측정

| 지표 | 질문 |
|---|---|
| Activation rate | 대상 session 중 protocol이 시작 전에 실행된 비율은? |
| Observation precision | 기록 중 실제 skill change로 이어질 고신호 항목은 몇 개인가? |
| Duplicate rate | 같은 문제를 반복 기록했는가? |
| Closure | actioned 항목이 open으로 남지 않았는가? |
| Context cost | session start scan이 체감 latency/context를 과도하게 늘렸는가? |

### 완료 조건

- [ ] 최소 1개 correction이 observation으로 남음
- [ ] staged diff와 원 observation을 연결할 수 있음
- [ ] 승인 전 live skill이 변경되지 않음
- [ ] 다음 실제 task에서 개선 효과를 검증함

## Project 2: Activation reliability test

### 목표

description matching만 사용할 때와 explicit instruction/hook을 함께 사용할 때의 activation 차이를 관찰한다.

### 시나리오

| 시작 prompt | 예상 위험 |
|---|---|
| 짧은 파일 목록 요청 | domain skill보다 background observer가 밀릴 수 있음 |
| 단순 질문에서 multi-step task로 확장 | 첫 turn에 observer가 없으면 초기 사건 누락 |
| 명시적 `task-observer` 언급 | 가장 강한 control case |
| workspace 없이 시작 | config file 자체가 context에 없을 수 있음 |

### 기록 양식

```text
session id:
activation tier:
prompt class:
skill loaded:
protocol executed:
checkpoint present:
observation path correct:
notes:
```

activation 여부와 protocol 실행 여부를 따로 측정한다.

## Project 3: Parallel session collision drill

### 목표

두 session이 거의 동시에 observation을 기록할 때 overwrite, duplicate ID, silent fork를 탐지한다.

### 절차

1. 동일한 stable workspace를 가리키는지 absolute path로 확인한다.
2. 두 session에서 서로 다른 observation을 동시에 생성한다.
3. 파일명 ID, YAML `id`, body 내용을 대조한다.
4. archive와 active directory를 포함해 ID uniqueness를 검사한다.
5. duplicate나 collision이 발생하면 upstream procedure에서 벗어난 지점을 찾는다.

> 실제 중요한 log에서 처음 시험하지 말고 disposable copy에서 수행한다.

## Project 4: Weekly review 운영

### 목표

open observation을 actionable staged update로 바꾸되, backlog 정리와 live mutation을 분리한다.

### Review board

| Observation | Target skill | 분류 | Confidentiality | 결정 | Staged path |
|---|---|---|---|---|---|
| 예: 배포 검증 누락 | deploy-skill | additive | public principle | action | `skill-updates/deploy-skill/` |
| 예: client 내부 endpoint 노출 | research-skill | internal | confidential | redact/generalize | - |

### Checklist

- [ ] current target skill과 대조
- [ ] duplicate/already-fixed 정리
- [ ] sibling/family propagation 검토
- [ ] public/internal boundary 확인
- [ ] additive/restructuring 분류
- [ ] staged bundle validation
- [ ] diff와 rollback 방법 제시
- [ ] 승인 후 설치
- [ ] 다음 task에 regression check 배정

## Project 5: Cross-cutting principle audit

### 목표

하나의 반복 교훈을 library 전체에 무작정 복사하지 않고, 적용 범위를 검증한다.

### 예시 원칙

> 중요한 query가 비어 있으면 “결과 없음”으로 결론 내리기 전에 query 자체가 정상 동작했는지 독립적으로 확인한다.

### Audit 질문

- 어떤 skill family에 실제로 적용되는가?
- 이미 동등한 규칙이 있는가?
- 문장 추가보다 script/validator/hook이 더 적절한가?
- false positive나 불필요한 latency를 만들지 않는가?
- confidential incident를 일반화하는 과정에서 민감 정보가 제거됐는가?

## Project 6: v2 → v3 migration rehearsal

### 목표

단일 `log.md`를 per-observation files로 변환하는 절차와 rollback을 검증한다.

### 안전 원칙

- 실제 log의 backup 또는 disposable copy에서 먼저 rehearsal한다.
- 설치한 release에 포함된 `scripts/migrate-log.py`와 migration reference를 사용한다.
- migration 전후 observation 수와 ID를 비교한다.
- 원본 rollback artifact가 보존됐는지 확인한다.
- 불명확한 parse 결과가 있으면 자동 진행하지 않는다.

## Sources

- [Weekly review reference](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/references/weekly-review.md)
- [Migration reference](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/references/migration.md)
- [v3.0.0 release notes](https://github.com/rebelytics/one-skill-to-rule-them-all/releases/tag/v3.0.0)
- [v3.2.0 release notes](https://github.com/rebelytics/one-skill-to-rule-them-all/releases/tag/v3.2.0)

