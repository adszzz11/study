---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# GitHub: cathrynlavery/diagram-design

> **한 줄 정의**: `cathrynlavery/diagram-design`은 AI coding agent가 prose·Mermaid·draw.io의 의미를 브랜드 맞춤형 **editorial diagram**으로 재구성해, build step 없는 HTML + inline SVG로 출력하도록 안내하는 오픈소스 Agent Skill이다.

## Overview

`diagram-design`은 Mermaid나 D2처럼 입력을 동일한 결과로 변환하는 deterministic renderer가 아니다. LLM에게 diagram type 선택, semantic simplification, brand token 적용, SVG layout, accessibility, pre-output quality check 절차를 제공하는 **prompt/reference/template package**다.

```text
요청 또는 기존 diagram
        ↓
SKILL.md에서 type 선택
        ↓
필요한 type reference만 로드
        ↓
semantic model + design tokens + layout
        ↓
HTML + inline SVG
        ↓ optional
SVG 추출 / PNG rasterization
```

핵심 목표는 일반적인 AI diagram의 과도한 rounded box, color, shadow, 획일적인 monospace를 줄이고, 낮은 density와 명확한 editorial hierarchy로 읽히는 결과를 만드는 것이다.

> [!warning] 문서 수량 불일치
> 2026-08-12 조사 기준 GitHub repository 설명은 **29 types**, README 본문과 gallery 설명은 **27 types**라고 표시한다. 저장소가 빠르게 갱신되므로 실제 도입 시 사용할 commit의 파일 목록을 확인한다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, 설계 철학, 핵심 특징
- [ ] [[02-ecosystem|Ecosystem]] — Mermaid, D2, draw.io, Figma와의 역할 비교
- [ ] [[03-references|References]] — 공식 문서와 검증 지점
- [ ] [[04-learning/01-getting-started|Getting Started]] — clone, 첫 prompt, 결과 검수
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — progressive disclosure, token, import pipeline
- [ ] [[05-projects|Projects]] — architecture redraw와 brand onboarding 실습
- [ ] [[cheatsheet|Cheatsheet]] — 선택 기준, output dial, checklist 빠른 참조

## When To Use

- 문서·slide·landing page에 넣을 **브랜드 일관성 있는 editorial diagram**이 필요할 때
- prose 요구사항에서 architecture, sequence, process, strategy diagram을 탐색적으로 만들 때
- Mermaid나 draw.io의 semantic content는 유지하되 audience에 맞게 다시 디자인할 때
- framework와 runtime dependency 없이 전달 가능한 HTML + inline SVG가 필요할 때
- agent에게 density, connector, typography, accessibility 규칙을 일관되게 적용시키고 싶을 때

## When Not To Use

- 같은 source에서 항상 동일한 결과가 필요한 deterministic build/CI pipeline
- Mermaid source를 그대로 보존하고 자동 render만 해야 하는 문서 시스템
- pixel-perfect draw.io round-trip이나 원본 coordinate·palette 보존이 요구될 때
- 고빈도 interactive chart, live dashboard, 대규모 data visualization이 필요할 때
- agent 판단 없이 GUI에서 직접 세밀하게 편집하는 workflow가 중심일 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[../ripgrep/README|ripgrep]] — repository와 reference file을 빠르게 탐색할 때 함께 쓰는 CLI

## Sources

- [GitHub repository](https://github.com/cathrynlavery/diagram-design)
- [README](https://github.com/cathrynlavery/diagram-design/blob/main/README.md)
- [Agent Skill specification](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/SKILL.md)
- [Commit history](https://github.com/cathrynlavery/diagram-design/commits/main/)
- [Security Policy](https://github.com/cathrynlavery/diagram-design/blob/main/SECURITY.md)

