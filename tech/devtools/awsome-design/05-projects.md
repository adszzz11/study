---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# awesome-design-md — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## Project 1. Reference 비교와 Direction Brief

### 목표

서로 다른 category에서 reference 3개를 골라 브랜드 이름이 아닌 design property로 비교한다.

| 비교 항목 | 기록할 내용 |
|---|---|
| Typography | family, scale, weight, code treatment |
| Color | semantic role, accent frequency, status color |
| Layout | max width, grid, density, responsive breakpoint |
| Shape/depth | radius, border, shadow, layering |
| Components | button, input, navigation의 공통 규칙 |

### 산출물

- 1-page direction brief
- 유지/변형/제거할 원칙 표
- brand-specific asset과 IP risk 목록

### 완료 조건

- [ ] “어느 브랜드처럼”이 아니라 구체적 property로 방향을 설명한다.
- [ ] light/dark preview를 모두 비교한다.
- [ ] product context와 맞지 않는 요소를 명시적으로 제거한다.

## Project 2. Existing App용 DESIGN.md 만들기

### 목표

기존 UI의 CSS와 component를 inventory하고, 실제 구현과 일치하는 project `DESIGN.md` 초안을 만든다.

```text
CSS/component inventory
        ↓
primitive token 후보 추출
        ↓
semantic/component token 정리
        ↓
rationale와 Do/Don't 작성
        ↓
lint + visual review
```

### 작업 순서

1. hard-coded color, spacing, radius, font 값을 조사한다.
2. 중복 값을 무조건 합치지 말고 semantic role을 먼저 분류한다.
3. 대표 component의 default/hover/focus/disabled state를 기록한다.
4. 실제 구현과 desired direction의 차이를 migration backlog로 분리한다.
5. CLI lint 후 designer와 developer가 함께 review한다.

### 산출물

- `DESIGN.md`
- 현재 구현과 contract의 gap report
- 단계별 migration backlog

## Project 3. Tailwind/DTCG Export Pipeline

### 목표

하나의 `DESIGN.md`에서 web theme과 vendor-neutral token artifact를 생성한다.

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md export --format css-tailwind DESIGN.md > theme.css
npx @google/design.md export --format dtcg DESIGN.md > tokens.json
```

### CI checklist

- [ ] CLI exact version pinning
- [ ] `lint`와 `export` 분리
- [ ] generated artifact drift 검사
- [ ] export 결과의 consumer test
- [ ] CLI update 시 migration review

## Project 4. Agent UI 실험

### 목표

동일한 settings page를 세 조건으로 구현해 `DESIGN.md`의 효과를 비교한다.

| Variant | 제공 context |
|---|---|
| A | 기능 요구사항만 제공 |
| B | screenshot + 기능 요구사항 |
| C | project `DESIGN.md` + 기능 요구사항 |

### 평가 지표

- token 일치율
- component 재사용률
- 화면 간 spacing 일관성
- accessibility issue 수
- reviewer가 수정한 visual decision 수
- prompt에 반복한 design instruction 길이

> 결과는 agent의 일반적 우열이 아니라 해당 repository와 contract 품질에 대한 실험으로 해석한다.

## Project 5. Security·Accessibility Review Gate

### 목표

외부 reference 도입 시 자동 lint가 놓치는 위험을 review checklist로 보완한다.

```text
External DESIGN.md
  ├─ provenance / URL review
  ├─ irrelevant instruction removal
  ├─ brand/IP review
  ├─ schema lint
  ├─ component implementation
  └─ keyboard / focus / semantics / motion test
```

### 산출물

- reference provenance record
- brand/IP review note
- manual keyboard test 결과
- screen reader smoke test 결과
- reduced motion과 responsive test 결과

## Sources

- https://github.com/VoltAgent/awesome-design-md
- https://github.com/google-labs-code/design.md
- https://www.w3.org/community/design-tokens/

