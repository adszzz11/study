---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# taste — Projects

> [[04-learning/02-deep-dive|이전: Deep dive]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: Cheatsheet]]

## 프로젝트 1: 기존 codebase에 맞는 작은 feature

### 목표

generic abstraction을 추가하지 않고 인접 code의 naming, error style, dependency, test pattern에 맞는 변경을 만든다.

### 절차

1. 대상 call-site, 인접 구현, 관련 test를 exemplar로 수집한다.
2. baseline prompt와 `taste` 적용 prompt로 각각 patch를 만든다.
3. 불필요한 file·class·config 수, test relevance, reviewer 수정량을 비교한다.

```text
Create the smallest change that matches the adjacent implementation.
Ground decisions in the opened call-sites and tests. Do not introduce a
new abstraction unless the existing code demonstrates the same pattern.
```

## 프로젝트 2: 외부 공개 decision memo

### 목표

독자가 첫 화면에서 결정, 근거, 필요한 행동을 파악하게 한다.

| Grounding | 자료 |
|---|---|
| Job | 승인을 얻을 결정 한 문장 |
| Reader | 이미 아는 맥락과 확인할 사실 |
| Exemplar | 최근 승인된 memo 1~2개 |
| Source | incident, metric, code/config |

평가 지표는 분량 자체보다 “독자가 다음 행동을 정확히 답하는가”로 둔다.

## 프로젝트 3: UI generated-tell audit

### 목표

기존 design system을 존중하면서 template reflex를 찾고 가장 작은 수정안을 제시한다.

- 실제 component와 token을 먼저 연다.
- primary action과 visual hierarchy를 한 문장으로 적는다.
- 3-card 반복, 의미 없는 gradient, 가짜 testimonial, 동일한 시각 무게를 찾는다.
- 새 design system을 만들지 말고 existing primitive로 수정한다.

## 프로젝트 4: Architecture proposal critique

### 목표

근거 없는 service, queue, cache를 제거하고 migration과 failure path를 전면에 둔다.

```text
Verdict → Invention → Cut → Miss → Tell → Fix
```

실제 config, deploy topology, incident, on-call 기록을 근거로 삼고 다음을 확인한다.

- [ ] 현재 constraint와 목표가 연결되는가?
- [ ] failure와 rollback이 표현됐는가?
- [ ] scale 숫자의 source가 있는가?
- [ ] 새 component가 실제 요구로 정당화되는가?

## 프로젝트 5: Blind evaluation

### 실험 설계

| 항목 | 방법 |
|---|---|
| Sample | 실제 작업 10개 이상, domain별 분산 |
| Variants | 동일 model의 baseline과 `taste` 적용본 |
| Blinding | reviewer에게 variant 정보를 숨김 |
| Measures | invention 수, 불필요 요소 수, task success, 수정 시간 |
| Controls | 같은 source, prompt goal, model/version, token budget |

공개 benchmark가 없으므로 이 실험이 adoption 판단의 핵심 근거가 된다. “더 세련돼 보임”만 묻지 말고 실제 오류와 reviewer effort를 기록한다.

## 완료 기준

- [ ] source와 exemplar가 재현 가능하게 기록됨
- [ ] baseline과 적용본이 동일 조건에서 생성됨
- [ ] deterministic check가 별도로 통과함
- [ ] practitioner review가 blind로 수행됨
- [ ] 유지·수정·제거 결정과 reversal condition이 남음

## Sources

- [Hmbown/taste README](https://github.com/Hmbown/taste#readme)
- [REVIEW.md](https://raw.githubusercontent.com/Hmbown/taste/main/references/REVIEW.md)
- [DOMAINS.md](https://raw.githubusercontent.com/Hmbown/taste/main/references/DOMAINS.md)

