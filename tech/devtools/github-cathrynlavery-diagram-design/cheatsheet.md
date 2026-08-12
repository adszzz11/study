---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Diagram Design — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## 정체

```text
Agent design policy ≠ deterministic renderer
semantic redraw ≠ pixel-level conversion
HTML + inline SVG = 기본 전달 형식
```

## 요청 template

```text
<시각화할 내용과 핵심 관계>

- diagram type: auto | architecture | sequence | ...
- audience: engineer | mixed | executive
- format: html | svg | png | html+png
- size: doc-inline | doc-wide | slide-16x9 | social-og | print preset
- detail: faithful | balanced | simplified
- style: default | website onboarding | manual tokens
```

## Type 빠른 선택

| 보여줄 것 | Type |
|---|---|
| component, boundary, dependency | Architecture |
| 시간순 message 교환 | Sequence |
| 분기와 작업 흐름 | Flowchart / Process |
| state와 transition | State machine |
| 책임 주체별 handoff | Swimlane |
| entity와 relation | ER/data model |
| hierarchy와 containment | Tree / Nested / Org chart |
| 전략적 position | Quadrant / Consultant 2×2 |
| 시간 계획 | Timeline / Gantt |
| 수치 비교·추세 | Bar / Line / Scatter |

## 핵심 design rule

| 항목 | Rule of thumb |
|---|---|
| Density | 목표 4/10, 한 diagram에 질문 하나 |
| Accent | focal element 1–2개만 |
| Color | `paper`, `ink`, `muted`, `accent`, `link` semantic token |
| Grid | coordinate·width·gap은 4px grid |
| Line | 1px hairline, shadow 금지 |
| Radius | 최대 10px |
| Connector | rounded orthogonal elbow, node 관통 금지 |
| Monospace | port, URL, field type 등 기술 정보에만 |
| SVG a11y | `role="img"`, `<title>`, `<desc>`, 고유 `aria-labelledby` |

## Website mapping

| Website | Token/role |
|---|---|
| body background | `paper` |
| primary text | `ink` |
| secondary text | `muted` |
| card background | `paper-2` |
| CTA/link color | `accent` |
| h1 font | title |
| body font | node name |
| code/pre font | technical sublabel |

## Import 원칙

```text
Mermaid/draw.io
→ bounded parser
→ nodes/edges/groups/cycles/hubs/fields
→ audience와 detail에 맞게 단순화
→ 4px-grid에서 redraw
→ fidelity ledger 작성
```

원본에서 기본적으로 보존하지 않는 것:

- coordinate와 node 위치
- palette와 decoration
- pixel-level shape
- 완전한 round-trip editability

## 최종 checklist

- [ ] 핵심 메시지가 한 문장으로 설명된다.
- [ ] type이 질문과 audience에 맞는다.
- [ ] label을 output preset의 실제 크기에서 읽을 수 있다.
- [ ] connector direction과 endpoint가 명확하다.
- [ ] color만으로 의미를 전달하지 않는다.
- [ ] semantic omission/merge를 fidelity ledger에 적었다.
- [ ] HTML/SVG에 build/runtime dependency가 숨어 있지 않다.
- [ ] source prompt, agent/model, commit SHA를 기록했다.

## 운영 주의

- 2026-08-12 기준 repository 설명 29 types, README/gallery 27 types로 불일치한다.
- versioned release가 없으므로 production에서는 commit SHA pinning 또는 fork를 사용한다.
- website fetch와 web font는 network 환경에 의존한다.
- managed update가 custom `style-guide.md`를 덮을 수 있다.

## Sources

- [Diagram Design README](https://github.com/cathrynlavery/diagram-design/blob/main/README.md)
- [SKILL.md](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/SKILL.md)
- [Onboarding spec](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/references/onboarding.md)
- [Security Policy](https://github.com/cathrynlavery/diagram-design/blob/main/SECURITY.md)
