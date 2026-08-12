---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Diagram Design — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

`cathrynlavery/diagram-design`은 AI coding agent용 **Agent Skill**이다. 자연어 또는 기존 Mermaid/draw.io diagram에서 의미를 추출하고, 목적과 audience에 맞는 diagram type 및 visual hierarchy를 선택해 HTML + inline SVG로 새로 그리도록 지시한다.

구성 요소의 역할은 다음과 같다.

| 구성 | 역할 |
|---|---|
| `skills/diagram-design/SKILL.md` | type selection, design philosophy, connector rule, 최종 checklist |
| `references/type-*.md` | diagram별 semantic model과 layout rule |
| `references/style-guide.md` | color·font token의 single source of truth |
| `assets/template*.html` | light/editorial output scaffold |
| `assets/example-*.html` | type 및 variant별 예제 |
| `scripts/*_extract.py` | Mermaid·draw.io를 bounded intermediate representation으로 추출 |
| `commands/`, `prompts/` | Claude Code 및 Pi 통합 |
| `.codex-plugin/`, `.claude-plugin/` | agent별 plugin metadata |

## Why

일반적인 LLM diagram은 정보 구조보다 익숙한 시각 패턴을 반복하기 쉽다.

- rounded rectangle가 과도하게 반복된다.
- accent color와 shadow가 hierarchy 없이 남용된다.
- 모든 label에 monospace를 써서 editorial typography가 약해진다.
- website나 제품의 brand language와 연결되지 않는다.
- 사용자가 Figma에서 다시 손보거나 결과를 버리게 된다.

Diagram Design은 이를 renderer 기능이 아닌 **agent design policy**로 다룬다. 무엇을 시각화할지 먼저 정하고, density 목표를 4/10 정도로 제한하며, accent를 1–2개 focal element에만 사용한다. 즉 “더 많이 그리기”보다 “무엇을 생략하고 강조할지 결정하기”가 핵심이다.

## 핵심 특징

### Progressive disclosure

Agent는 모든 reference를 한 번에 context에 넣지 않는다. `SKILL.md`를 index처럼 읽은 뒤 architecture 요청에는 `type-architecture.md`, sequence 요청에는 `type-sequence.md`처럼 관련 파일만 추가로 불러온다. README는 type·primitive·utility를 합쳐 **36 reference files**라고 설명한다.

### Opinionated design system

| 규칙 | 의도 |
|---|---|
| `paper`, `ink`, `muted`, `accent`, `link` semantic token | raw color가 아닌 역할 중심 styling |
| accent는 1–2개 focal element에만 사용 | 독자의 시선 유도 |
| Instrument Serif / Geist / Geist Mono 역할 분리 | title, node name, technical sublabel 구분 |
| 1px hairline, shadow 금지, radius 최대 10px | 장식보다 구조 강조 |
| coordinate·width·gap을 4px grid에 정렬 | 시각적 rhythm 유지 |
| rounded orthogonal elbow connector | diagonal line의 교차와 모호성 감소 |
| monospace는 port·URL·field type 등에만 사용 | 기술 정보의 의미 있는 구분 |
| `<svg role="img">`, `<title>`, `<desc>` | accessible name과 설명 제공 |

이 규칙 집합은 graphics library라기보다 결과물에 적용되는 **design lint contract**에 가깝다.

### 넓은 diagram 범위

README 본문 기준 27개 범주는 다음 영역을 포괄한다.

- Software/flow: Architecture, Flowchart, Sequence, State machine, ER/data model, Swimlane, Process, Data flow
- Structure: Nested, Tree, Org chart, Layer stack, Pyramid/Funnel
- Strategy/editorial: Quadrant, Consultant 2×2, Venn, Radar/Spider, Loop
- Time/data: Timeline, Gantt, Bar chart, Line chart, Scatter plot
- Enterprise/data platform: IT current-state, High-Level, Medallion, DP integration, DP security matrix

각 type은 원칙적으로 `minimal light`, `minimal dark`, `full-editorial` variant를 제공한다. 단, type 수는 repository 설명과 README가 일치하지 않으므로 commit 단위로 검증해야 한다.

## 운영 상태와 위험

- MIT License의 copyright 연도는 2025다.
- 2026-08-12 GitHub 화면 기준 약 7.2k stars, 476 forks, 41 commits다.
- 2026-08-10~12에도 sequence fragment, Pi 지원, import, accessibility, CI 관련 변경이 있었다.
- versioned release가 아직 없고 security fix는 최신 `main`만 지원한다.

> [!important] Production 사용
> 재현성과 공급망 통제를 위해 floating `main` 대신 검토한 commit SHA를 pin하거나 자체 fork를 운영한다.

## Sources

- [Repository](https://github.com/cathrynlavery/diagram-design)
- [README — Architecture](https://github.com/cathrynlavery/diagram-design/blob/main/README.md#architecture)
- [README — What it makes](https://github.com/cathrynlavery/diagram-design/blob/main/README.md#what-it-makes)
- [SKILL.md](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/SKILL.md)
- [LICENSE](https://github.com/cathrynlavery/diagram-design/blob/main/LICENSE)
- [Security Policy](https://github.com/cathrynlavery/diagram-design/blob/main/SECURITY.md)

