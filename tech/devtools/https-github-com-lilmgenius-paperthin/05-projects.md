---
date: 2026-08-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Paperthin — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1: README clean-v0 실험

### 목표

변경 이력처럼 누적된 README를 현재 사용자가 필요한 내용만 남도록 정리하고 `re0`의 no-op invariant를 관찰한다.

### 절차

- [ ] 작은 repository와 대상 README를 고른다.
- [ ] 현재 truth, stale delta, duplication, scaffolding residue를 표시한다.
- [ ] `re0`를 적용한다.
- [ ] before/after에서 정보 손실과 중복 감소를 review한다.
- [ ] 이미 깨끗한 두 번째 문서에는 no-op 하는지 확인한다.

### 성공 기준

| 지표 | 기준 |
|---|---|
| 현재 사용법 보존 | 설치·실행·제약이 남음 |
| stale narrative 제거 | 과거 migration 설명이 본문을 지배하지 않음 |
| 변경 절제 | 개선이 없으면 diff가 없음 |

## Project 2: SSOT drift audit

### 목표

version, supported target, feature roster처럼 여러 파일에 복제된 사실을 canonical source로 수렴시킨다.

```bash
rg -n 'version|supported|catalog|skills' .
```

- [ ] 같은 claim이 등장하는 파일과 consumer를 표로 만든다.
- [ ] source of truth 하나를 선택한다.
- [ ] 가능한 consumer는 canonical source에서 생성/참조하게 한다.
- [ ] CI에 drift check를 추가한다.
- [ ] 사람이 읽는 문서에는 source 위치를 명시한다.

## Project 3: Evaluation leakage lab

### 목표

동일한 prompt/context를 공유한 generator와 evaluator가 잘못된 결과를 서로 승인하는 상황을 재현한다.

1. 애매한 요구로 작은 artifact를 생성한다.
2. 같은 framing을 준 evaluator에게 점수를 매기게 한다.
3. 공식 specification, executable test, 실제 user surface 중 하나를 external ground truth로 추가한다.
4. `mandela` 관점에서 평가가 어떻게 달라지는지 기록한다.

> 여러 model을 썼다는 사실만으로 independence가 생기지 않는다. source와 framing의 독립성을 확인한다.

## Project 4: Evidence-driven iteration

### 목표

작은 web/API 기능을 `re0-loop`로 두 cycle 운영한다.

| 단계 | 산출물 |
|---|---|
| `FRAME` | user-visible 성공 기준 |
| `BUILD` | 최소 구현과 automated test |
| `DRIVE` | browser/HTTP 실제 surface evidence |
| `RE0-MEMO` | 다음 cycle에 필요한 학습 |
| `HATE` | 치명적 objection 하나와 cheap test |
| `RE0-WORK` | 다음 action 하나 |

완료 판단은 생성 파일 수가 아니라 성공 기준을 직접 지지하는 evidence로 한다.

## Project 5: Safe catalog upgrade drill

- [ ] disposable environment에 일부 skill만 설치한다.
- [ ] `/re0-upgrade`가 제안하는 add/remove/change plan을 기록한다.
- [ ] confirmation 전 filesystem이 변하지 않는지 확인한다.
- [ ] 승인 후 manifest와 실제 directory가 28-skill catalog로 수렴하는지 확인한다.
- [ ] rollback 또는 재설치 경로를 문서화한다.

## 회고 질문

- skill이 없었다면 놓쳤을 문제는 무엇인가?
- procedure 비용이 결과 개선보다 컸던 순간은 언제인가?
- external evidence는 정말 generator의 framing에서 독립적이었는가?
- 다음에는 자동 trigger와 명시 호출 중 무엇이 더 안전한가?

## Sources

- https://github.com/LilMGenius/paperthin/blob/main/skills/depth/re0/SKILL.md
- https://github.com/LilMGenius/paperthin/blob/main/skills/coil/re0-loop/SKILL.md
- https://github.com/LilMGenius/paperthin/blob/main/skills/breadth/re0-upgrade/SKILL.md

