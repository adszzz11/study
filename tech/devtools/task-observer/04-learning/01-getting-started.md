---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Task Observer — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 목표

처음부터 전체 skill library를 자동 개선하려 하지 말고, 한 개의 stable workspace와 소수 skill로 pilot을 시작한다. 성공 기준은 “설치 파일이 존재함”이 아니라 다음 세 가지다.

- 새 session에서 Task Observer가 첫 tool call 전에 활성화된다.
- observation이 지정한 absolute path에 유효한 YAML로 생성된다.
- review 결과가 live skill을 직접 덮어쓰지 않고 staging에 남는다.

## 1. Bundle 확인

공식 repository의 같은 release에서 bundle 전체를 가져온다.

```text
task-observer/
├── SKILL.md
├── references/
└── scripts/
```

`SKILL.md`만 복사하면 migration, validation, 환경별 절차가 빠진 degraded install이 된다. 설치 위치와 방식은 사용하는 agent client의 Agent Skills 문서를 따른다.

## 2. Stable workspace 선택

observation storage는 매번 사라지는 temporary directory나 ephemeral worktree가 아니라 지속되는 absolute path여야 한다.

```text
/absolute/stable/workspace/
├── skill-observations/
│   ├── observation-log/
│   │   └── archive/
│   ├── cross-cutting-principles.md
│   ├── skill-families.md
│   ├── last-review-date.txt
│   └── checkpoints.log
└── skill-updates/
```

주의할 점:

- path에 공백이 있을 수 있으므로 shell에서 항상 quote한다.
- 여러 workspace를 운영한다면 anchor workspace와 각 log의 관계를 문서화한다.
- 기존 populated log 옆에 두 번째 empty log를 만들어 silent fork하지 않는다.

## 3. Activation을 두 겹으로 구성

### Skill metadata

description은 “무엇을 하는가”뿐 아니라 “언제 사용해야 하는가”를 구체적으로 표현해야 한다. 이것은 discovery/trigger 후보를 강화하지만 실행 보장은 아니다.

### Client/harness instruction

사용 환경에 따라 다음 중 가능한 방법을 사용한다.

- `CLAUDE.md` 또는 `AGENTS.md`에 session-start activation instruction 추가
- user-level preference에 항상 적용되는 trigger 추가
- harness의 `SessionStart` hook 사용
- 명시적 skill invocation 사용

단순히 “skill을 load하라”가 아니라 **Session Start Protocol을 실행하라**고 써야 한다. 파일을 읽고 protocol을 실행하지 않는 상태는 activation 성공이 아니다.

## 4. 새 session에서 검증

설치에 사용한 session이 아니라 완전히 새 session에서 검증한다.

```text
검증용 task 시작
  → Task Observer invocation 확인
  → stable absolute workspace 확인
  → checkpoints.log 또는 동등한 실행 흔적 확인
  → 의도적 correction/reusable pattern 발생
  → observation file 생성 확인
```

Observation 예시 구조:

```markdown
---
id: 1
status: open
skill: example-skill
type: improve-skill
date: 2026-09-20
title: "Validate deployment before declaring success"
---

## Issue

변경 후 배포 상태를 확인하지 않고 완료를 선언했다.

## Improvement

완료 직전에 deployment status 확인 단계를 추가한다.

## Principle

완료 선언은 최신 외부 상태 검증에 근거해야 한다.
```

정확한 schema와 필수 field는 설치한 release의 `references/observation-log.md`를 따른다. 위 예시는 개념 설명용이며 upstream template을 대체하지 않는다.

## 5. 첫 review 연습

작은 backlog로 다음 순서를 연습한다.

1. open observation을 target skill의 현재 내용과 대조한다.
2. duplicate, 이미 해결됨, 잘못 분류된 항목을 정리한다.
3. confidential/internal context가 공개 skill에 들어가지 않는지 확인한다.
4. additive fix인지 restructuring/new skill인지 분류한다.
5. 변경안을 `skill-updates/`에 staging한다.
6. bundle validation과 diff를 확인한다.
7. 사용자가 승인한 뒤 설치한다.
8. 다음 session에서 activation과 개선 효과를 검증한다.

## 실패 진단

| 증상 | 가능한 원인 | 확인 |
|---|---|---|
| skill이 load되지 않음 | description matching under-trigger | explicit invocation과 client instruction 비교 |
| load됐지만 기록 없음 | Session Start Protocol 미실행 | checkpoint와 workspace 생성 여부 확인 |
| backlog가 항상 비어 있음 | 잘못된 relative path, path word splitting | absolute path와 quoting 확인 |
| YAML scan 실패 | prose value 미인용, 잘못된 header | YAML parser/validator 실행 |
| 같은 관찰이 반복됨 | 적용 후 status/reconciliation 누락 | staged path와 resolution 확인 |
| parallel session에서 충돌 | shared monolithic log 또는 ID race | per-file store와 release 지침 확인 |

## Pilot 완료 기준

- [ ] bundle 전체가 동일 release로 설치됨
- [ ] stable absolute workspace가 하나로 고정됨
- [ ] 새 session에서 activation과 protocol 실행 확인
- [ ] 최소 1개 observation 생성 및 YAML validation 통과
- [ ] review → staging → approval 경계 확인
- [ ] live skill 적용 후 다음 session에서 재검증

## Sources

- [Task Observer user guide](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/USER-GUIDE.md)
- [Environment and activation reference](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/references/environments.md)
- [Observation log reference](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/references/observation-log.md)
- [Agent Skills specification](https://agentskills.io/specification)

