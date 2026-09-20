---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# taste — Overview

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: Ecosystem]]

## What

`taste`는 code를 실행하거나 artifact를 자동 채점하는 프로그램이 아니다. Agent Skills compatible client가 읽는 `SKILL.md`와 reference 문서로 구성된 **instruction-only skill**이다. Agent가 생성 또는 critique 작업을 시작할 때 실제 근거를 먼저 찾고, 목적에 맞는 형태와 완성도를 선택하도록 유도한다.

```text
taste/
├── SKILL.md
├── references/
│   ├── DOMAINS.md
│   └── REVIEW.md
├── agents/openai.yaml
├── assets/taste-icon.svg
└── scripts/
    ├── install.sh
    └── package-claude-skill.sh
```

## Why

### 겨냥하는 실패

| 실패 | 증상 | `taste`의 교정 |
|---|---|---|
| Grounding 부족 | 실제 code나 memo 대신 model memory로 답함 | repository의 실제 exemplar를 먼저 연다 |
| Invention | source에 없는 가격·기능·정책을 채움 | 빈칸을 우회하거나 `[confirm: …]`로 표시한다 |
| Flat hierarchy | 중요도가 다른 항목을 같은 크기로 나열 | impact를 rank한 뒤 공간을 배분한다 |
| Template reflex | hero–3 cards–FAQ–CTA, 관습적 문서 intro | artifact의 job에 맞춰 shape를 정한다 |
| Over-finishing | stakes보다 지나치게 길고 정교함 | 독자가 다음 polish를 알아채지 못하면 멈춘다 |

초기판의 폭넓은 원칙과 scorecard는 최신 model이 이미 아는 내용과 중복됐다. v1.0은 `grounding`, `specificity`, `finish calibration`이라는 더 좁은 실패 지점에 집중한다.

## 핵심 특징

### 1. Grounding 먼저

Create와 Critique 모두 다음 세 사실을 확정한다.

1. **The job** — 누구에게 어떤 행동을 일으켜야 하는가?
2. **Reader knowledge** — 독자가 이미 아는 것과 검증할 것은 무엇인가?
3. **The exemplar** — 어떤 인접 code, 실제 page, memo, token, data를 기준으로 삼을 것인가?

### 2. Shape follows the job

관습적인 형식을 먼저 고르지 않는다. 목적에 따라 짧은 memo, table, chart, function, module, single screen 중 필요한 형식을 선택한다.

### 3. Rank, then allocate

결과에 미치는 영향이 큰 결정부터 정렬하고, 중요한 항목에 더 많은 attention과 화면·문서 공간을 준다.

### 4. Specifics come from the source

source에 없는 사실은 만들지 않는다. 불확실성이 결과를 막으면 명시적으로 표시한다.

```text
[confirm: pricing tiers]
[confirm: retention policy]
```

### 5. 하나의 recommendation

여러 무난한 선택지를 늘어놓는 대신 기본 recommendation 하나와 그 결정을 뒤집을 조건 하나를 제시한다.

## 적용 범위와 한계

- code, UI, documents, data/charts, systems에 공통 workflow를 적용한다.
- instruction-only이므로 test, lint, accessibility audit를 대체하지 않는다.
- project-specific 규칙을 자동으로 학습하거나 저장하지 않는다.
- 공개 benchmark나 blind before/after evaluation이 없어 직접 효과를 검증해야 한다.
- repository 이력이 짧고 packaged release와 source metadata가 어긋날 수 있다.

## Sources

- [Hmbown/taste README](https://github.com/Hmbown/taste#readme)
- [Hmbown/taste SKILL.md](https://raw.githubusercontent.com/Hmbown/taste/main/SKILL.md)
- [DOMAINS.md](https://raw.githubusercontent.com/Hmbown/taste/main/references/DOMAINS.md)

