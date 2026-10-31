---
date: 2026-08-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Paperthin — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Paperthin은 coding agent가 반복해서 실패하는 지점에 짧고 재사용 가능한 operating procedure를 삽입하는 Agent Skills library다. 각 skill은 YAML frontmatter와 Markdown instruction을 담은 `SKILL.md`이며, 필요하면 `scripts/`, `references/`, `assets/`를 함께 둔다.

```text
paperthin/
├── skills/
│   ├── depth/      # 한 artifact, claim, decision
│   ├── breadth/    # 여러 파일과 설치 surface
│   ├── coil/       # 여러 iteration의 장기 cycle
│   └── mesh/       # 복수의 독립 관점
├── scripts/        # catalog, discovery notice, validation adapter
├── .claude-plugin/ # plugin manifest와 skill catalog
├── .github/workflows/
└── docs/
```

## Why

AI coding agent의 실패는 code generation 능력 부족만으로 생기지 않는다.

| 실패 형태 | 결과 | Paperthin의 대응 |
|---|---|---|
| additive bias | 낡은 문서에 patch와 설명이 계속 누적됨 | `re0`가 현재 진실만 남기는 clean v0로 재작성 |
| duplicated truth | 같은 사실이 여러 파일에서 drift | `ssotize`가 canonical source로 통합 |
| request misread | 잘못 읽은 목표를 일관되게 완성 | `readchk`가 ambiguity를 다시 점검 |
| evaluation leakage | 생성자와 evaluator가 같은 framing을 공유 | `mandela`가 external ground truth 유입을 검사 |
| false progress | 파일 수·기능 수·작업 시간이 진척도로 오인됨 | `re0-loop`, `nba`가 evidence와 next action 중심으로 전환 |
| vendor leakage | model/CLI 이름이 durable docs에 고착 | `detool` 계열 discipline으로 portability 유지 |

## 핵심 특징

### 네 가지 scope

| 계층 | 적용 범위 | 대표 skill | 질문 |
|---|---|---|---|
| `depth` | 한 artifact/claim/plan | `re0`, `factchk`, `hate`, `sip` | 이 결과물 자체가 깨끗하고 검증됐는가? |
| `breadth` | 여러 파일/설치 surface | `ssotize`, `re0-upgrade` | 흩어진 상태가 하나의 truth로 수렴하는가? |
| `coil` | 장기 iteration | `re0-loop`, `re0-memo`, `re0-work`, `nba` | 다음 cycle에 무엇을 보존하고 실행할까? |
| `mesh` | 복수 독립 lens | `prism` | 합의가 가린 divergence는 무엇인가? |

### 대표 reflex

- `re0`: 전체 artifact를 읽고 stale delta, duplication, scaffolding residue를 제거한다. 고칠 것이 없으면 바꾸지 않는다.
- `factchk`: 가능/불가능에 대한 직감을 모두 외부 source로 검증한다.
- `hate`: plan을 무너뜨릴 수 있는 load-bearing objection 하나와 가장 싼 test를 찾는다.
- `sip`: artifact 직후 필요한 QA reflex를 route하며 Git/commit은 건드리지 않는다.
- `re0-loop`: `FRAME → BUILD → DRIVE → RE0-MEMO → HATE → RE0-WORK → BUILD AGAIN`을 반복한다.
- `prism`: 한 대상에 독립 lens를 적용해 성급한 consensus보다 divergence를 찾는다.

## 프로젝트 성숙도 읽기

- `v0.17.4`, 28 skills, MIT license는 실제 사용 가능한 catalog임을 보여준다.
- signed tag와 provenance-oriented release workflow는 supply-chain 신뢰를 높이려는 신호다.
- 약 158 stars와 21 forks는 관심의 지표일 뿐 품질 benchmark가 아니다.
- 현재 핵심 가치는 “검증된 성능 제품”보다 명시적이고 재사용 가능한 agent operating discipline에 있다.

## Sources

- https://github.com/LilMGenius/paperthin#the-problem
- https://github.com/LilMGenius/paperthin#the-index
- https://github.com/LilMGenius/paperthin/blob/main/.claude-plugin/plugin.json
- https://github.com/LilMGenius/paperthin/blob/main/LICENSE

