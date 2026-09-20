---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Task Observer — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Task Observer는 task 수행 중 나타나는 고신호 사건을 **observation**으로 남기고, 이를 review하여 Agent Skill의 새 버전이나 새 skill 후보로 만드는 meta-skill이다.

관찰 대상은 세 가지다.

| 유형 | 신호 | 결과 후보 |
|---|---|---|
| New skill | 반복 가능한 multi-step workflow인데 대응 skill이 없음 | 새 skill 초안 |
| Improve skill | correction, 빠진 edge case, 잘못된 assumption, 더 나은 workflow | 기존 skill diff |
| Simplify skill | 사용되지 않는 규칙, 중복·모순, 실행되지 않는 장황한 지침 | 삭제·통합·구조적 enforcement |

반대로 단발성 수정, 이미 저장된 preference, 방법론과 무관한 tool bug는 원칙적으로 기록하지 않는다. 즉 transcript archive가 아니라 **skill lifecycle에 영향을 주는 사건만 선별하는 event store**다.

## Why

Agent Skills 표준은 `SKILL.md`, `scripts/`, `references/`, `assets/`를 이용한 packaging과 progressive disclosure를 정의한다. 그러나 다음 문제는 별도로 남는다.

- skill을 발견했다고 해서 실제 session에서 반드시 활성화되는 것은 아니다.
- 실행 중 얻은 correction과 workaround가 다음 버전에 자동으로 반영되지 않는다.
- skill은 작성 시점의 snapshot으로 낡기 쉽다.
- 공통 원칙이 여러 skill에 중복되거나 서로 모순될 수 있다.
- 개선이 기억과 수동 회고에 의존한다.
- parallel session이 한 개의 공유 log를 덮어쓰면 collision 위험이 생긴다.

Task Observer는 이를 observation → review → staging → approval → validation lifecycle로 다룬다. 중요한 경계는 **관찰 결과가 곧바로 live instruction이 되지 않는 것**이다.

## 핵심 아키텍처

### Progressive-disclosure bundle

```text
task-observer/
├── SKILL.md
├── references/
│   ├── environments.md
│   ├── observation-log.md
│   ├── signals.md
│   ├── skill-authoring.md
│   ├── weekly-review.md
│   ├── migration.md
│   └── starter-principles.md
└── scripts/
    ├── migrate-log.py
    └── validate-skill-bundle.py
```

metadata는 discovery에, `SKILL.md`는 핵심 절차에, references/scripts는 해당 episode에만 사용한다. 다만 `2026-09-20` 기준 upstream `SKILL.md`는 800줄을 넘으므로, Agent Skills specification의 500줄 이하 권장과 비교해 context cost를 평가해야 한다.

### Dual-layer activation

Task Observer는 첫 tool call 이전에 활성화되어야 session 전체를 관찰할 수 있다.

- 1차: skill metadata의 강한 trigger description
- 2차: `CLAUDE.md`, `AGENTS.md`, user preference 또는 harness `SessionStart` hook의 명시적 activation

설치 성공은 파일 존재가 아니라 **새 session에서 실제 invocation과 observation workspace 초기화가 확인되는가**로 판정한다. `discovery ≠ activation`은 Task Observer만의 결함이 아니라 현재 Agent Skills 생태계의 구조적 문제다.

### Session Start Protocol

1. ephemeral worktree가 아닌 stable absolute workspace를 정한다.
2. observation storage와 bundle integrity를 확인한다.
3. observation body 전체가 아닌 YAML frontmatter를 scan한다.
4. active cross-cutting principles를 읽는다.
5. 마지막 review가 7일 이상 지났고 open observation이 있으면 review를 제안한다.
6. staged update가 이미 설치되거나 대체되었는지 reconcile한다.

### Per-observation event store

```text
skill-observations/
├── observation-log/
│   ├── 0001-research-source-validation.md
│   ├── 0002-deployment-check-missing.md
│   └── archive/
├── cross-cutting-principles.md
├── skill-families.md
├── last-review-date.txt
└── checkpoints.log
```

각 observation은 YAML frontmatter와 `Issue`, `Improvement`, `Principle`을 가진다. 대표 status는 `open`, `actioned`, `declined`, `superseded`, `parked`이며, `parked`는 명시된 외부 선행조건이 있을 때만 사용한다.

## 특징과 trade-off

| 특징 | 이점 | 비용·주의 |
|---|---|---|
| 파일 기반 저장 | inspectable, diffable, portable | path·permission·backup 운영 필요 |
| observation별 파일 | parallel write collision 감소 | ID allocation과 archive 규칙 필요 |
| frontmatter scan | backlog가 커져도 context 절약 | YAML validity 검증 필요 |
| cross-cutting principles | skill library 전체 quality floor 상승 | 과잉 일반화와 기밀 유출 주의 |
| staging + approval | 자동 self-modification 위험 감소 | review/install discipline 필요 |
| dual-layer activation | under-trigger 가능성 감소 | client/harness별 설정 차이 존재 |

## Release 흐름

| 버전 | 날짜 | 핵심 변화 |
|---|---:|---|
| `v2.0.0` | 2026-07-17 | monolithic skill을 progressive-disclosure 구조로 분리 |
| `v3.0.0` | 2026-08-28 | per-observation files, migration, activation hardening |
| `v3.1.0` | 2026-09-04 | absolute path, shell portability, validation, starter principles 강화 |
| `v3.2.0` | 2026-09-11 | multi-log aggregate review, parseable YAML 점검, non-Latin slug 보존, checkpoint 강화 |

## 근거 해석 시 주의

maintainer는 7개월 동안 78개 skill에서 약 1,400개 observation을 기록했다고 설명한다. 이는 장기간 실제 사용 사례로는 의미가 있지만, 통제된 독립 benchmark나 일반화 가능한 생산성 수치는 아니다.

## Sources

- [Task Observer README](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/README.md)
- [Task Observer SKILL.md](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/SKILL.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [Task Observer releases](https://github.com/rebelytics/one-skill-to-rule-them-all/releases)
- [Environment and activation reference](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/references/environments.md)

