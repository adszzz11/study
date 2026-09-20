---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Task Observer — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## 한눈에 보기

```text
Observe → Log → Review → Stage → Validate → Approve → Install → Verify
```

| 항목 | 빠른 답 |
|---|---|
| 정체 | continuous skill improvement meta-skill |
| 저장 | local Markdown + YAML, observation당 한 파일 |
| 관찰 | 전체 task session과 post-task feedback |
| review | 기본적으로 주기적, open backlog 중심 |
| 변경 | live skill이 아니라 `skill-updates/`에 staging |
| 승인 | human approval 후 install |
| 최신 확인 | `v3.2.0`, 2026-09-11 |

## 기록할 것

- reusable multi-step workflow인데 skill이 없음 → **New skill**
- 사용자 correction, 빠진 edge case, 틀린 assumption → **Improve skill**
- 중복·모순·실행되지 않는 장황한 규칙 → **Simplify skill**
- 여러 skill에 적용되는 교훈 → **Cross-cutting principle 후보**

## 기록하지 않을 것

- 단발성 task 수정
- 이미 저장된 preference의 반복
- skill methodology와 무관한 tool bug
- transcript 전체나 민감한 원문
- 근거 없는 “언젠가 유용할 것” 메모

## Session Start

- [ ] stable absolute workspace 확인
- [ ] 기존 populated log 탐색; silent fork 방지
- [ ] bundle integrity 확인
- [ ] observation YAML frontmatter만 우선 scan
- [ ] active cross-cutting principles 읽기
- [ ] 7일 이상 + open backlog이면 review 제안
- [ ] staged update reconciliation
- [ ] protocol 실행 흔적/checkpoint 확인

## Observation 최소 의미 구조

```markdown
---
id: 42
status: open
skill: example-skill
type: improve-skill
date: 2026-09-20
title: "Quote paths containing spaces"
---

## Issue
무엇이 잘못되거나 반복됐는가?

## Improvement
skill을 어떻게 바꿔야 하는가?

## Principle
다른 project에도 적용되는 일반 원리는 무엇인가?
```

> 실제 필수 field와 명명법은 설치한 version의 `references/observation-log.md`를 따른다.

## Status

| 상태 | 사용 시점 |
|---|---|
| `open` | review/action 대기 |
| `actioned` | 적용 또는 staged resolution 완료 |
| `declined` | 검토 후 미적용 결정 |
| `superseded` | 다른 관찰/변경으로 대체 |
| `parked` | 명시된 외부 선행조건으로 보류 |

## Review

- [ ] target skill 현재 상태와 대조
- [ ] duplicate/already-fixed 제거
- [ ] skill family/sibling 적용 범위 확인
- [ ] public/internal confidentiality 분리
- [ ] additive fix vs restructuring 분류
- [ ] cross-cutting principle 적용 여부 확인
- [ ] staged path 기록
- [ ] bundle validation과 diff 확인
- [ ] rollback 방법 제시
- [ ] 사용자 승인 후 설치
- [ ] 다음 실제 task에서 검증

## Activation 진단

| 문제 | 점검 |
|---|---|
| 발견되지만 실행 안 됨 | `discovery ≠ activation`; explicit instruction/hook 확인 |
| 첫 사건이 누락됨 | 첫 tool call 전 activation 여부 확인 |
| load됐지만 protocol 미실행 | checkpoint와 workspace initialization 확인 |
| 특정 client에서만 실패 | 환경별 activation tier와 config visibility 확인 |

## Storage 진단

| 문제 | 점검 |
|---|---|
| backlog가 비어 보임 | absolute path, existence count, YAML parse 확인 |
| path에 공백 | 모든 shell expansion quote, word splitting 금지 |
| 중복 ID | active + archive + ID floor를 포함한 allocation 절차 확인 |
| 같은 개선 반복 | `status`, `resolution`, staged path reconciliation 확인 |
| 병렬 overwrite | monolithic log가 아닌 per-observation file인지 확인 |

## 경계 문장

- Task Observer는 **memory 전체**가 아니다.
- Task Observer는 **runtime telemetry**가 아니다.
- Task Observer는 **background daemon**이 아니다.
- observation은 **자동으로 live rule이 되지 않는다**.
- maintainer 사용량은 **독립 benchmark가 아니다**.

## Sources

- [Task Observer repository](https://github.com/rebelytics/one-skill-to-rule-them-all)
- [Task Observer SKILL.md](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/SKILL.md)
- [Observation log reference](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/references/observation-log.md)
- [Weekly review reference](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/references/weekly-review.md)
- [v3.2.0 release notes](https://github.com/rebelytics/one-skill-to-rule-them-all/releases/tag/v3.2.0)
